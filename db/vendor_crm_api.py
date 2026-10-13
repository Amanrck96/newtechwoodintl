"""Vendor <-> Admin CRM Router and Business Logic.
Handles vendor requests lifecycle, activity tracking, SLA calculations, Vendor 360, notifications, and strict server-side scoping.
"""
import os
import json
import sqlite3
from datetime import datetime, date

try:
    from db.notifications import (
        send_notification,
        get_user_notifications,
        mark_notification_read,
        get_unread_count
    )
except ImportError:
    from notifications import (
        send_notification,
        get_user_notifications,
        mark_notification_read,
        get_unread_count
    )

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ntw_crm.db")

ALLOWED_REQUEST_TYPES = [
    "Sample request",
    "Quote / price request",
    "Technical consultation / site visit",
    "Order (PO) request",
    "CAD / specification request",
    "Support / complaint"
]

ALLOWED_STATUSES = [
    "New",
    "In Review",
    "Quoted/Approved",
    "In Progress",
    "Completed",
    "Rejected",
    "Cancelled"
]

def _api():
    import api_router
    return api_router

def get_connection(db_path=None):
    path = db_path or os.environ.get("CRM_DB_FILE") or DB_FILE
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def is_vendor(user):
    return user and user.get("role") in ("architect", "dealer")

def is_admin_or_sales(user):
    return user and user.get("role") in ("admin", "superadmin", "sales")

def calculate_sla(due_date_str, status):
    """
    Computes SLA indicator:
    - green: on-time or completed
    - amber: due within 2 days
    - red: overdue
    """
    if status in ("Completed", "Rejected", "Cancelled"):
        return {"color": "green", "label": "Resolved", "badge_class": "badge-success"}
    if not due_date_str:
        return {"color": "green", "label": "No SLA set", "badge_class": "badge-secondary"}
    try:
        due = datetime.strptime(due_date_str[:10], "%Y-%m-%d").date()
        today = date.today()
        days_left = (due - today).days
        if days_left < 0:
            return {"color": "red", "label": f"Overdue by {abs(days_left)}d", "badge_class": "badge-danger", "days_left": days_left}
        elif days_left <= 2:
            return {"color": "amber", "label": f"Due in {days_left}d", "badge_class": "badge-warning", "days_left": days_left}
        else:
            return {"color": "green", "label": f"{days_left}d left", "badge_class": "badge-success", "days_left": days_left}
    except Exception:
        return {"color": "green", "label": due_date_str, "badge_class": "badge-info"}

def generate_req_number(conn):
    """Generate sequential collision-safe request ref number like REQ-2026-0001."""
    current_year = date.today().year
    prefix = f"REQ-{current_year}-"
    cur = conn.cursor()
    cur.execute("SELECT ref_no FROM vendor_requests WHERE ref_no LIKE ? ORDER BY id DESC LIMIT 1", (f"{prefix}%",))
    row = cur.fetchone()
    if row and row["ref_no"]:
        try:
            last_seq = int(row["ref_no"].split("-")[-1])
            new_seq = last_seq + 1
        except Exception:
            new_seq = 1
    else:
        new_seq = 1
    return f"{prefix}{new_seq:04d}"

# ─────────────────────────────────────────────────────────────
# HTTP HANDLER ROUTER BRIDGE
# ─────────────────────────────────────────────────────────────

def route(handler, method, path, qs=None, body=None, db_path=None):
    """
    HTTP route handler called from api_router.py.
    Returns True if handled, False if not matched.
    """
    # Check if path belongs to vendor CRM or notifications
    is_crm_path = (
        path == "/api/vendor-requests" or
        path.startswith("/api/vendor-requests/") or
        path == "/api/admin/vendor-inbox" or
        path.startswith("/api/admin/vendor-360") or
        path == "/api/notifications" or
        path.startswith("/api/notifications/")
    )
    if not is_crm_path:
        return False

    api = _api()
    auth_user = api.get_auth_user(handler)
    if not auth_user:
        api.send_json(handler, {"error": "Authentication required"}, 401)
        return True

    # 1. Notifications endpoints
    if path == "/api/notifications" and method == "GET":
        unread_only = qs.get("unread", ["0"])[0] == "1" if qs else False
        notifs = get_user_notifications(auth_user["id"], unread_only=unread_only, db_path=db_path)
        unread_c = get_unread_count(auth_user["id"], db_path=db_path)
        api.send_json(handler, {"success": True, "notifications": notifs, "unread_count": unread_c})
        return True

    if path == "/api/notifications/count" and method == "GET":
        unread_c = get_unread_count(auth_user["id"], db_path=db_path)
        api.send_json(handler, {"success": True, "unread_count": unread_c})
        return True

    if path == "/api/notifications/read" and method in ("POST", "PUT"):
        body = body or {}
        notif_id = body.get("id")
        if notif_id:
            mark_notification_read(notif_id, user_id=auth_user["id"], db_path=db_path)
        api.send_json(handler, {"success": True, "message": "Marked read"})
        return True

    # 2. Admin Vendor Inbox
    if path == "/api/admin/vendor-inbox" and method == "GET":
        if not is_admin_or_sales(auth_user):
            api.send_json(handler, {"error": "Access forbidden: Admin or Sales role required"}, 403)
            return True
        params = {k: v[0] for k, v in (qs or {}).items()}
        status_code, data = get_vendor_inbox(params, db_path=db_path)
        api.send_json(handler, data, status_code)
        return True

    # 3. Vendor 360 View
    if path.startswith("/api/admin/vendor-360/") and method == "GET":
        if not is_admin_or_sales(auth_user):
            api.send_json(handler, {"error": "Access forbidden: Admin or Sales role required"}, 403)
            return True
        vendor_id = path.split("/api/admin/vendor-360/")[1].strip("/")
        status_code, data = get_vendor_360(vendor_id, db_path=db_path)
        api.send_json(handler, data, status_code)
        return True

    # 4. Export Requests (CSV)
    if path == "/api/vendor-requests/export" and method == "GET":
        params = {k: v[0] for k, v in (qs or {}).items()}
        status_code, data = export_requests_csv(params, auth_user, db_path=db_path)
        if status_code == 200:
            csv_bytes = data["csv"].encode("utf-8")
            handler.send_response(200)
            handler.send_header("Content-Type", "text/csv; charset=utf-8")
            handler.send_header("Content-Disposition", f'attachment; filename="{data["filename"]}"')
            handler.send_header("Content-Length", str(len(csv_bytes)))
            handler.send_header("Access-Control-Allow-Origin", "*")
            handler.end_headers()
            handler.wfile.write(csv_bytes)
        else:
            api.send_json(handler, data, status_code)
        return True

    # 5. Comments on Request
    if path.startswith("/api/vendor-requests/") and path.endswith("/comment") and method == "POST":
        req_id = path.split("/")[3]
        status_code, data = add_request_comment(req_id, body or {}, auth_user, db_path=db_path)
        api.send_json(handler, data, status_code)
        return True

    # 5b. Status, Assign, Cancel sub-routes on Request
    if path.startswith("/api/vendor-requests/") and (path.endswith("/status") or path.endswith("/assign") or path.endswith("/cancel")):
        req_id = path.split("/")[3]
        if path.endswith("/cancel") and method in ("POST", "PUT"):
            status_code, data = update_request(req_id, {"status": "Cancelled", "comment": (body or {}).get("comment", "Request cancelled")}, auth_user, db_path=db_path)
        elif method in ("PUT", "PATCH", "POST"):
            status_code, data = update_request(req_id, body or {}, auth_user, db_path=db_path)
        else:
            status_code, data = 405, {"error": "Method not allowed"}
        api.send_json(handler, data, status_code)
        return True

    # 6. Attachments on Request
    if path.startswith("/api/vendor-requests/") and path.endswith("/attachments"):
        req_id = path.split("/")[3]
        if method == "GET":
            status_code, data = get_request_attachments(req_id, auth_user, db_path=db_path)
        else:
            status_code, data = add_request_attachment(req_id, body or {}, auth_user, db_path=db_path)
        api.send_json(handler, data, status_code)
        return True

    # 7. Single Request: GET, PUT/PATCH, DELETE
    parts = path.split("/")
    if len(parts) == 4 and parts[1] == "api" and parts[2] == "vendor-requests":
        req_id = parts[3]
        if method == "GET":
            status_code, data = get_single_request(req_id, auth_user, db_path=db_path)
        elif method in ("PUT", "PATCH"):
            status_code, data = update_request(req_id, body or {}, auth_user, db_path=db_path)
        elif method == "DELETE":
            status_code, data = delete_request(req_id, auth_user, db_path=db_path)
        else:
            status_code, data = 405, {"error": "Method not allowed"}
        api.send_json(handler, data, status_code)
        return True

    # 8. Collection: GET /api/vendor-requests, POST /api/vendor-requests
    if path == "/api/vendor-requests":
        if method == "GET":
            params = {k: v[0] for k, v in (qs or {}).items()}
            status_code, data = list_requests(params, auth_user, db_path=db_path)
        elif method == "POST":
            status_code, data = create_request(body or {}, auth_user, db_path=db_path)
        else:
            status_code, data = 405, {"error": "Method not allowed"}
        api.send_json(handler, data, status_code)
        return True

    api.send_json(handler, {"error": f"Endpoint not found: {method} {path}"}, 404)
    return True

# ─────────────────────────────────────────────────────────────
# LOGIC IMPLEMENTATIONS
# ─────────────────────────────────────────────────────────────

def list_requests(params, auth_user, db_path=None):
    """List requests with strict server-side scoping."""
    conn = get_connection(db_path)
    cur = conn.cursor()

    query = """
        SELECT vr.*,
               u.full_name as vendor_name,
               u.email as vendor_email,
               u.role as vendor_role,
               u.vendor_id as vendor_code,
               a.full_name as assigned_to_name,
               p.name as linked_product_name,
               (SELECT COUNT(*) FROM request_activity WHERE request_id = vr.id) as activity_count
        FROM vendor_requests vr
        LEFT JOIN users u ON vr.vendor_user_id = u.id
        LEFT JOIN users a ON vr.assigned_to = a.id
        LEFT JOIN products p ON vr.linked_product_id = p.id
        WHERE 1=1
    """
    args = []

    # Strict server-side scoping
    if is_vendor(auth_user):
        query += " AND vr.vendor_user_id = ?"
        args.append(auth_user["id"])
    else:
        # Admin or sales filters
        vendor_filter = params.get("vendor_id")
        if vendor_filter:
            query += " AND vr.vendor_user_id = ?"
            args.append(vendor_filter)

    status_filter = params.get("status")
    if status_filter and status_filter.lower() != "all":
        query += " AND vr.status = ?"
        args.append(status_filter)

    type_filter = params.get("type")
    if type_filter and type_filter.lower() != "all":
        query += " AND vr.type = ?"
        args.append(type_filter)

    priority_filter = params.get("priority")
    if priority_filter and priority_filter.lower() != "all":
        query += " AND vr.priority = ?"
        args.append(priority_filter)

    assigned_filter = params.get("assigned_to")
    if assigned_filter:
        query += " AND vr.assigned_to = ?"
        args.append(assigned_filter)

    search = params.get("search")
    if search:
        query += " AND (vr.ref_no LIKE ? OR vr.title LIKE ? OR vr.details LIKE ?)"
        s = f"%{search}%"
        args.extend([s, s, s])

    query += " ORDER BY vr.created_at DESC"

    cur.execute(query, args)
    rows = cur.fetchall()
    conn.close()

    items = []
    for r in rows:
        item = dict(r)
        item["sla"] = calculate_sla(item.get("due_date"), item.get("status"))
        items.append(item)

    return 200, {
        "success": True,
        "requests": items,
        "count": len(items),
        "user_role": auth_user.get("role")
    }

def create_request(body, auth_user, db_path=None):
    """Create a new vendor request with collision-safe ref_no."""
    req_type = body.get("type")
    title = body.get("title", "").strip()
    details = body.get("details", "").strip()
    priority = body.get("priority", "Medium")
    if isinstance(priority, str):
        priority = priority.capitalize()
        if priority not in ("Low", "Medium", "High", "Urgent"):
            priority = "Medium"
    due_date = body.get("due_date")
    linked_product_id = body.get("linked_product_id")
    linked_order_id = body.get("linked_order_id")

    if not title:
        return 400, {"success": False, "error": "Request title is required"}
    if req_type not in ALLOWED_REQUEST_TYPES:
        return 400, {"success": False, "error": f"Invalid request type. Must be one of: {', '.join(ALLOWED_REQUEST_TYPES)}"}

    # Vendor scoping: vendor creates for self, admin can specify vendor_user_id
    if is_vendor(auth_user):
        vendor_user_id = auth_user["id"]
        assigned_to = None
    else:
        vendor_user_id = body.get("vendor_user_id") or auth_user["id"]
        assigned_to = body.get("assigned_to")

    conn = get_connection(db_path)
    cur = conn.cursor()
    ref_no = generate_req_number(conn)

    cur.execute("""
        INSERT INTO vendor_requests (
            ref_no, vendor_user_id, type, title, details, priority,
            status, assigned_to, due_date, linked_product_id, linked_order_id,
            created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, 'New', ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (
        ref_no, vendor_user_id, req_type, title, details, priority,
        assigned_to, due_date, linked_product_id, linked_order_id
    ))
    new_id = cur.lastrowid

    # Create initial activity
    cur.execute("""
        INSERT INTO request_activity (
            request_id, actor_id, action, from_status, to_status, comment, is_internal, created_at
        ) VALUES (?, ?, 'created', NULL, 'New', 'Request created', 0, CURRENT_TIMESTAMP)
    """, (new_id, auth_user["id"]))

    conn.commit()
    conn.close()

    # Trigger notification to admin team
    send_notification(
        user_id="admin",
        title=f"New Vendor Request: {ref_no}",
        message=f"{auth_user.get('full_name', 'Vendor')} submitted {req_type}: '{title}'",
        channel="all",
        metadata={"ref_no": ref_no, "request_id": new_id, "type": req_type},
        db_path=db_path
    )

    return 201, {
        "success": True,
        "id": new_id,
        "ref_no": ref_no,
        "request": {"id": new_id, "ref_no": ref_no},
        "message": f"Request {ref_no} submitted successfully"
    }

def get_single_request(req_id, auth_user, db_path=None):
    """Retrieve single request and timeline with strict scoping."""
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
        SELECT vr.*,
               u.full_name as vendor_name,
               u.email as vendor_email,
               u.role as vendor_role,
               u.phone as vendor_phone,
               u.vendor_id as vendor_code,
               a.full_name as assigned_to_name,
               a.email as assigned_to_email,
               p.name as linked_product_name,
               p.category as linked_product_category,
               o.order_number as linked_order_number
        FROM vendor_requests vr
        LEFT JOIN users u ON vr.vendor_user_id = u.id
        LEFT JOIN users a ON vr.assigned_to = a.id
        LEFT JOIN products p ON vr.linked_product_id = p.id
        LEFT JOIN waltz_orders o ON vr.linked_order_id = o.id
        WHERE vr.id = ?
    """, (req_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return 404, {"success": False, "error": "Request not found"}

    item = dict(row)

    # Strict scoping check: vendor can only view their own
    if is_vendor(auth_user) and item["vendor_user_id"] != auth_user["id"]:
        conn.close()
        return 403, {"success": False, "error": "Access forbidden: You may only view your own requests"}

    # Fetch activity timeline
    act_query = """
        SELECT ra.*, u.full_name as actor_name, u.role as actor_role
        FROM request_activity ra
        LEFT JOIN users u ON ra.actor_id = u.id
        WHERE ra.request_id = ?
    """
    act_args = [req_id]

    # Hide internal notes from vendors
    if is_vendor(auth_user):
        act_query += " AND ra.is_internal = 0"

    act_query += " ORDER BY ra.created_at ASC"
    cur.execute(act_query, act_args)
    activities = [dict(a) for a in cur.fetchall()]

    # Fetch attachments
    cur.execute("SELECT * FROM request_attachments WHERE request_id = ? ORDER BY created_at DESC", (req_id,))
    attachments = [dict(att) for att in cur.fetchall()]

    conn.close()

    item["sla"] = calculate_sla(item.get("due_date"), item.get("status"))
    item["activities"] = activities
    item["attachments"] = attachments
    return 200, {"success": True, "request": item}

def update_request(req_id, body, auth_user, db_path=None):
    """
    Update request status, assignment, or details.
    Vendor restriction: Vendor can ONLY change status to 'Cancelled' while status is 'New'.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM vendor_requests WHERE id = ?", (req_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return 404, {"success": False, "error": "Request not found"}

    current = dict(row)

    # Scoping check for vendor
    if is_vendor(auth_user):
        if current["vendor_user_id"] != auth_user["id"]:
            conn.close()
            return 403, {"success": False, "error": "Access forbidden: You cannot modify another vendor's request"}

        # Vendor may only cancel if New
        requested_status = body.get("status")
        if requested_status:
            if requested_status != "Cancelled":
                conn.close()
                return 403, {"success": False, "error": "Vendors may only cancel requests"}
            if current["status"] != "New":
                conn.close()
                return 400, {"success": False, "error": f"Cannot cancel request in '{current['status']}' status. Only 'New' requests can be cancelled."}

            comment = body.get("comment") or "Request cancelled by vendor"
            cur.execute("""
                UPDATE vendor_requests
                SET status = 'Cancelled', updated_at = CURRENT_TIMESTAMP, closed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (req_id,))
            cur.execute("""
                INSERT INTO request_activity (
                    request_id, actor_id, action, from_status, to_status, comment, is_internal, created_at
                ) VALUES (?, ?, 'cancelled', ?, 'Cancelled', ?, 0, CURRENT_TIMESTAMP)
            """, (req_id, auth_user["id"], current["status"], comment))
            conn.commit()
            conn.close()
            return 200, {"success": True, "message": "Request cancelled successfully", "status": "Cancelled"}
        else:
            conn.close()
            return 403, {"success": False, "error": "Vendors cannot modify request parameters once submitted"}

    # Admin / Sales update flow
    new_status = body.get("status", current["status"])
    if new_status not in ALLOWED_STATUSES:
        conn.close()
        return 400, {"success": False, "error": f"Invalid status '{new_status}'. Allowed: {', '.join(ALLOWED_STATUSES)}"}

    assigned_to = body.get("assigned_to", current["assigned_to"])
    priority = body.get("priority", current["priority"])
    due_date = body.get("due_date", current["due_date"])
    comment = body.get("comment", "")
    is_internal = int(body.get("is_internal", 0))

    closed_at = current["closed_at"]
    if new_status in ("Completed", "Rejected", "Cancelled") and not closed_at:
        closed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        UPDATE vendor_requests
        SET status = ?, assigned_to = ?, priority = ?, due_date = ?, closed_at = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (new_status, assigned_to, priority, due_date, closed_at, req_id))

    # Log activity if status changed or assigned
    if new_status != current["status"]:
        act_comment = comment or f"Status changed from {current['status']} to {new_status}"
        cur.execute("""
            INSERT INTO request_activity (
                request_id, actor_id, action, from_status, to_status, comment, is_internal, created_at
            ) VALUES (?, ?, 'status_change', ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (req_id, auth_user["id"], current["status"], new_status, act_comment, is_internal))

        # Notify vendor of status change
        send_notification(
            user_id=current["vendor_user_id"],
            title=f"Update on {current['ref_no']}: {new_status}",
            message=f"Your request '{current['title']}' status was updated to '{new_status}'. {comment}".strip(),
            channel="all",
            metadata={"ref_no": current["ref_no"], "status": new_status, "request_id": req_id},
            db_path=db_path
        )

    elif assigned_to != current["assigned_to"]:
        cur.execute("""
            INSERT INTO request_activity (
                request_id, actor_id, action, from_status, to_status, comment, is_internal, created_at
            ) VALUES (?, ?, 'assigned', ?, ?, ?, 1, CURRENT_TIMESTAMP)
        """, (req_id, auth_user["id"], current["status"], current["status"], f"Assigned to {assigned_to}", 1))

    conn.commit()
    conn.close()
    return 200, {"success": True, "message": "Request updated successfully", "status": new_status}

def add_request_comment(req_id, body, auth_user, db_path=None):
    """Add a public or internal comment to a request."""
    comment = body.get("comment", "").strip()
    if not comment:
        return 400, {"success": False, "error": "Comment cannot be empty"}

    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM vendor_requests WHERE id = ?", (req_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return 404, {"success": False, "error": "Request not found"}

    req = dict(row)

    # Scoping check
    if is_vendor(auth_user):
        if req["vendor_user_id"] != auth_user["id"]:
            conn.close()
            return 403, {"success": False, "error": "Access forbidden: You cannot comment on another vendor's request"}
        is_internal = 0  # Vendors can NEVER post internal notes
    else:
        is_internal = 1 if body.get("is_internal") else 0

    cur.execute("""
        INSERT INTO request_activity (
            request_id, actor_id, action, from_status, to_status, comment, is_internal, created_at
        ) VALUES (?, ?, 'comment', ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (req_id, auth_user["id"], req["status"], req["status"], comment, is_internal))

    # Update request updated_at timestamp
    cur.execute("UPDATE vendor_requests SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (req_id,))

    conn.commit()
    conn.close()

    # If vendor commented, notify admin/assigned
    if is_vendor(auth_user):
        send_notification(
            user_id="admin",
            title=f"New reply on {req['ref_no']}",
            message=f"{auth_user.get('full_name')}: {comment[:100]}",
            channel="all",
            metadata={"ref_no": req["ref_no"], "request_id": req_id},
            db_path=db_path
        )
    elif not is_internal:
        # Admin posted a public comment -> notify vendor
        send_notification(
            user_id=req["vendor_user_id"],
            title=f"Admin reply on {req['ref_no']}",
            message=comment[:100],
            channel="all",
            metadata={"ref_no": req["ref_no"], "request_id": req_id},
            db_path=db_path
        )

    return 201, {"success": True, "message": "Comment added successfully"}

def add_request_attachment(req_id, body, auth_user, db_path=None):
    """Attach a document/file record to a request."""
    file_name = body.get("file_name", "attachment")
    file_url = body.get("file_url", "")
    file_size = body.get("file_size", 0)

    if not file_url:
        return 400, {"success": False, "error": "Attachment file_url is required"}

    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT vendor_user_id FROM vendor_requests WHERE id = ?", (req_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return 404, {"success": False, "error": "Request not found"}

    if is_vendor(auth_user) and row["vendor_user_id"] != auth_user["id"]:
        conn.close()
        return 403, {"success": False, "error": "Access forbidden"}

    cur.execute("""
        INSERT INTO request_attachments (request_id, file_name, file_url, file_size, uploaded_by, created_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (req_id, file_name, file_url, file_size, auth_user["id"]))
    att_id = cur.lastrowid
    conn.commit()
    conn.close()
    return 201, {"success": True, "attachment_id": att_id, "file_name": file_name}

def get_request_attachments(req_id, auth_user, db_path=None):
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT vendor_user_id FROM vendor_requests WHERE id = ?", (req_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return 404, {"success": False, "error": "Request not found"}

    if is_vendor(auth_user) and row["vendor_user_id"] != auth_user["id"]:
        conn.close()
        return 403, {"success": False, "error": "Access forbidden"}

    cur.execute("SELECT * FROM request_attachments WHERE request_id = ? ORDER BY created_at DESC", (req_id,))
    attachments = [dict(r) for r in cur.fetchall()]
    conn.close()
    return 200, {"success": True, "attachments": attachments}

def get_vendor_inbox(params, db_path=None):
    """
    Request Inbox for Admin/Sales with unread/New badge count,
    SLA traffic lights, and multi-criteria filters.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()

    # Summary metrics
    cur.execute("SELECT COUNT(*) FROM vendor_requests")
    total_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM vendor_requests WHERE status = 'New'")
    new_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM vendor_requests WHERE status = 'In Review'")
    in_review_count = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) FROM vendor_requests
        WHERE status NOT IN ('Completed', 'Rejected', 'Cancelled')
        AND due_date IS NOT NULL AND due_date < date('now')
    """)
    overdue_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM vendor_requests WHERE priority = 'Urgent' AND status NOT IN ('Completed', 'Rejected', 'Cancelled')")
    urgent_count = cur.fetchone()[0]

    # Query items
    query = """
        SELECT vr.*,
               u.full_name as vendor_name,
               u.email as vendor_email,
               u.role as vendor_role,
               u.vendor_id as vendor_code,
               a.full_name as assigned_to_name,
               p.name as linked_product_name,
               (SELECT COUNT(*) FROM request_activity WHERE request_id = vr.id) as activity_count
        FROM vendor_requests vr
        LEFT JOIN users u ON vr.vendor_user_id = u.id
        LEFT JOIN users a ON vr.assigned_to = a.id
        LEFT JOIN products p ON vr.linked_product_id = p.id
        WHERE 1=1
    """
    args = []

    vendor = params.get("vendor_id")
    if vendor:
        query += " AND vr.vendor_user_id = ?"
        args.append(vendor)

    status = params.get("status")
    if status and status.lower() != "all":
        query += " AND vr.status = ?"
        args.append(status)

    priority = params.get("priority")
    if priority and priority.lower() != "all":
        query += " AND vr.priority = ?"
        args.append(priority)

    assigned = params.get("assigned_to")
    if assigned:
        query += " AND vr.assigned_to = ?"
        args.append(assigned)

    is_overdue = params.get("overdue")
    if is_overdue == "1":
        query += " AND vr.due_date IS NOT NULL AND vr.due_date < date('now') AND vr.status NOT IN ('Completed', 'Rejected', 'Cancelled')"

    query += " ORDER BY vr.created_at DESC"
    cur.execute(query, args)
    rows = cur.fetchall()
    conn.close()

    items = []
    for r in rows:
        item = dict(r)
        item["sla"] = calculate_sla(item.get("due_date"), item.get("status"))
        items.append(item)

    return 200, {
        "success": True,
        "stats": {
            "total": total_count,
            "new": new_count,
            "in_review": in_review_count,
            "overdue": overdue_count,
            "urgent": urgent_count
        },
        "requests": items
    }

def get_vendor_360(vendor_id, db_path=None):
    """
    Vendor 360 page data:
    Profile, all requests, orders, meetings, invitations, total business value, avg response time.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("SELECT id, full_name, email, role, phone, vendor_id, avatar_initials, created_at FROM users WHERE id = ? OR vendor_id = ?", (vendor_id, vendor_id))
    vendor_row = cur.fetchone()
    if not vendor_row:
        conn.close()
        return 404, {"success": False, "error": f"Vendor '{vendor_id}' not found"}

    profile = dict(vendor_row)

    # 1. Requests
    cur.execute("""
        SELECT vr.*,
               a.full_name as assigned_to_name,
               p.name as linked_product_name
        FROM vendor_requests vr
        LEFT JOIN users a ON vr.assigned_to = a.id
        LEFT JOIN products p ON vr.linked_product_id = p.id
        WHERE vr.vendor_user_id = ?
        ORDER BY vr.created_at DESC
    """, (vendor_id,))
    requests = []
    response_times = []
    for r in cur.fetchall():
        item = dict(r)
        item["sla"] = calculate_sla(item.get("due_date"), item.get("status"))
        requests.append(item)

        # Calculate response time from created_at to first activity by an admin
        cur.execute("""
            SELECT created_at FROM request_activity
            WHERE request_id = ? AND actor_id != ?
            ORDER BY created_at ASC LIMIT 1
        """, (item["id"], vendor_id))
        act = cur.fetchone()
        if act and item.get("created_at"):
            try:
                t1 = datetime.strptime(item["created_at"][:19], "%Y-%m-%d %H:%M:%S")
                t2 = datetime.strptime(act["created_at"][:19], "%Y-%m-%d %H:%M:%S")
                hours = (t2 - t1).total_seconds() / 3600.0
                if hours >= 0:
                    response_times.append(hours)
            except Exception:
                pass

    avg_response_hours = round(sum(response_times) / len(response_times), 1) if response_times else 0.0

    # 2. Orders linked to this vendor
    cur.execute("""
        SELECT * FROM waltz_orders
        WHERE vendor_user_id = ?
        ORDER BY order_date DESC
    """, (vendor_id,))
    orders = [dict(o) for o in cur.fetchall()]
    total_order_value = sum(float(o.get("final_amount") or 0.0) for o in orders)

    # 3. Meetings linked to this vendor
    cur.execute("""
        SELECT * FROM meetings
        WHERE vendor_user_id = ?
        ORDER BY meeting_date DESC
    """, (vendor_id,))
    meetings = [dict(m) for m in cur.fetchall()]

    # 4. Invitations linked to this vendor
    cur.execute("""
        SELECT * FROM id_invitations
        WHERE vendor_user_id = ?
        ORDER BY created_at DESC
    """, (vendor_id,))
    invitations = [dict(i) for i in cur.fetchall()]

    # Last activity across any entity
    last_activity = None
    dates = []
    if requests:
        dates.append(requests[0].get("updated_at") or requests[0].get("created_at"))
    if orders:
        dates.append(orders[0].get("order_date"))
    if meetings:
        dates.append(meetings[0].get("meeting_date"))
    if dates:
        dates.sort(reverse=True)
        last_activity = dates[0]

    conn.close()

    open_requests = [r for r in requests if r["status"] not in ("Completed", "Rejected", "Cancelled")]
    closed_requests = [r for r in requests if r["status"] in ("Completed", "Rejected", "Cancelled")]

    return 200, {
        "success": True,
        "vendor": profile,
        "profile": profile,
        "total_business_value": total_order_value,
        "orders_count": len(orders),
        "open_requests_count": len(open_requests),
        "closed_requests_count": len(closed_requests),
        "avg_response_time_hours": avg_response_hours,
        "metrics": {
            "total_requests": len(requests),
            "open_requests": len(open_requests),
            "closed_requests": len(closed_requests),
            "total_orders": len(orders),
            "total_business_value": total_order_value,
            "avg_response_time_hours": avg_response_hours,
            "last_activity_date": last_activity
        },
        "requests": requests,
        "orders": orders,
        "meetings": meetings,
        "invitations": invitations
    }

def export_requests_csv(params, auth_user, db_path=None):
    """Export vendor requests to CSV format."""
    status_code, data = list_requests(params, auth_user, db_path)
    if status_code != 200:
        return status_code, data

    requests = data.get("requests", [])
    csv_rows = ["Ref No,Vendor,Type,Title,Priority,Status,Assigned To,Due Date,SLA,Created At"]
    for r in requests:
        ref = r.get("ref_no", "")
        vendor = (r.get("vendor_name") or "").replace(",", " ")
        rtype = (r.get("type") or "").replace(",", " ")
        title = (r.get("title") or "").replace(",", " ").replace('"', '""')
        prio = r.get("priority", "")
        st = r.get("status", "")
        assigned = (r.get("assigned_to_name") or "Unassigned").replace(",", " ")
        due = r.get("due_date") or ""
        sla_label = (r.get("sla", {}).get("label") or "").replace(",", " ")
        created = r.get("created_at") or ""
        csv_rows.append(f'"{ref}","{vendor}","{rtype}","{title}","{prio}","{st}","{assigned}","{due}","{sla_label}","{created}"')

    csv_content = "\n".join(csv_rows)
    return 200, {
        "success": True,
        "csv": csv_content,
        "filename": f"vendor_requests_{date.today().isoformat()}.csv"
    }

def delete_request(req_id, auth_user, db_path=None):
    """Only superadmin or admin can hard-delete a request."""
    if not auth_user or auth_user.get("role") not in ("admin", "superadmin"):
        return 403, {"success": False, "error": "Access forbidden: Only Administrators can delete requests"}

    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM vendor_requests WHERE id = ?", (req_id,))
    changes = conn.total_changes
    conn.commit()
    conn.close()

    if changes == 0:
        return 404, {"success": False, "error": "Request not found"}
    return 200, {"success": True, "message": "Request deleted"}
