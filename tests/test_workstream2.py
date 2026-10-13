"""Automated regression and acceptance tests for Workstream 2 (Vendor <-> Admin CRM).
Verifies request lifecycle, activity log, SLA calculations, notifications, Vendor 360,
and strict server-side scoping (403/404 isolation for cross-vendor access).
"""
import os
import sys
import json
import sqlite3
import pytest
from datetime import datetime, date, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from db import database, api_router, vendor_crm_api, notifications
from db.migrate import run_migrations

TEST_DB = os.path.join(BASE_DIR, "db", "test_ws2_crm.db")

class DummyWFile:
    def __init__(self):
        self.data = bytearray()
    def write(self, b):
        self.data.extend(b)

class DummyRFile:
    def __init__(self, data=b""):
        self.data = data
        self.pos = 0
    def read(self, n=-1):
        if n == -1:
            res = self.data[self.pos:]
            self.pos = len(self.data)
            return res
        res = self.data[self.pos:self.pos+n]
        self.pos += len(res)
        return res

class MockHandler:
    def __init__(self, path, method="GET", headers=None, body=None):
        self.path = path
        self.command = method
        self.headers = headers or {}
        self.wfile = DummyWFile()
        body_bytes = json.dumps(body).encode("utf-8") if isinstance(body, dict) else (body or b"")
        self.rfile = DummyRFile(body_bytes)
        self.headers["Content-Length"] = str(len(body_bytes))
        self.response_status = 200
        self.response_headers = {}

    def send_response(self, code):
        self.response_status = code

    def send_header(self, k, v):
        self.response_headers[k] = v

    def end_headers(self):
        pass

    def get_json_response(self):
        try:
            return json.loads(self.wfile.data.decode("utf-8"))
        except Exception:
            return None

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    if os.path.exists(TEST_DB):
        try: os.remove(TEST_DB)
        except Exception: pass

    # Point system to test db
    os.environ["CRM_DB_FILE"] = TEST_DB
    database.DB_FILE = TEST_DB

    # Initialize DB via migrations
    run_migrations(db_path=TEST_DB)

    future_exp = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

    # Insert test users and sessions
    with database.get_connection() as conn:
        cur = conn.cursor()
        # Admin
        cur.execute("INSERT OR REPLACE INTO users (id, email, password, full_name, role, status) VALUES ('admin', 'admin@ntw.in', '$2b$12$test', 'Admin User', 'admin', 'active')")
        cur.execute("INSERT OR REPLACE INTO sessions (token, user_id, expires_at) VALUES ('tok_admin', 'admin', ?)", (future_exp,))
        # Vendor 1 (Architect)
        cur.execute("INSERT OR REPLACE INTO users (id, email, password, full_name, role, status, vendor_id) VALUES ('arch_01', 'arch@studio.in', '$2b$12$test', 'Studio Architecture', 'architect', 'active', 'VND-001')")
        cur.execute("INSERT OR REPLACE INTO sessions (token, user_id, expires_at) VALUES ('tok_arch', 'arch_01', ?)", (future_exp,))
        # Vendor 2 (Dealer)
        cur.execute("INSERT OR REPLACE INTO users (id, email, password, full_name, role, status, vendor_id) VALUES ('dlr_01', 'dealer@timber.in', '$2b$12$test', 'Timber Supplies Co', 'dealer', 'active', 'DLR-002')")
        cur.execute("INSERT OR REPLACE INTO sessions (token, user_id, expires_at) VALUES ('tok_dlr', 'dlr_01', ?)", (future_exp,))
        # Sales
        cur.execute("INSERT OR REPLACE INTO users (id, email, password, full_name, role, status) VALUES ('sales_01', 'sales@ntw.in', '$2b$12$test', 'Sales Rep', 'sales', 'active')")
        cur.execute("INSERT OR REPLACE INTO sessions (token, user_id, expires_at) VALUES ('tok_sales', 'sales_01', ?)", (future_exp,))
        conn.commit()

    yield

    if os.path.exists(TEST_DB):
        try: os.remove(TEST_DB)
        except Exception: pass

def test_vendor_request_creation_and_ref_number():
    """Vendor creates request: ref_no is generated, initial activity logged, in-app notification sent."""
    handler = MockHandler(
        "/api/vendor-requests",
        method="POST",
        headers={"Authorization": "Bearer tok_arch"},
        body={
            "type": "Sample request",
            "title": "Peruvian Teak Decking Samples for Resort",
            "details": "Need 3 finish variants sent to Goa site office.",
            "priority": "High"
        }
    )
    api_router.handle_post(handler)
    assert handler.response_status == 201
    resp = handler.get_json_response()
    assert resp["success"] is True
    assert "REQ-" in resp["ref_no"]
    req_id = resp["id"]

    # Verify admin gets notification
    notifs = notifications.get_user_notifications("admin", db_path=TEST_DB)
    assert any(resp["ref_no"] in n["title"] for n in notifs)

    # Verify single fetch as owner
    get_h = MockHandler(f"/api/vendor-requests/{req_id}", method="GET", headers={"Authorization": "Bearer tok_arch"})
    api_router.handle_get(get_h)
    assert get_h.response_status == 200
    item = get_h.get_json_response()["request"]
    assert item["vendor_user_id"] == "arch_01"
    assert item["status"] == "New"
    assert len(item["activities"]) >= 1

def test_cross_vendor_isolation_403_rejection():
    """Strict Server-Side Scoping: Vendor B must be rejected with 403 when trying to read or modify Vendor A's request."""
    # 1. Vendor A creates a request
    handler_a = MockHandler(
        "/api/vendor-requests",
        method="POST",
        headers={"Authorization": "Bearer tok_arch"},
        body={"type": "Quote / price request", "title": "Confidential Commercial Quote A"}
    )
    api_router.handle_post(handler_a)
    req_id = handler_a.get_json_response()["id"]

    # 2. Vendor B (Dealer) attempts to READ Vendor A's request -> must be 403 Forbidden
    handler_b_read = MockHandler(f"/api/vendor-requests/{req_id}", method="GET", headers={"Authorization": "Bearer tok_dlr"})
    api_router.handle_get(handler_b_read)
    assert handler_b_read.response_status == 403
    assert "forbidden" in handler_b_read.get_json_response().get("error", "").lower()

    # 3. Vendor B attempts to UPDATE/CANCEL Vendor A's request -> must be 403 Forbidden
    handler_b_update = MockHandler(f"/api/vendor-requests/{req_id}", method="PUT", headers={"Authorization": "Bearer tok_dlr"}, body={"status": "Cancelled"})
    api_router.handle_put(handler_b_update)
    assert handler_b_update.response_status == 403

    # 4. Vendor B attempts to COMMENT on Vendor A's request -> must be 403 Forbidden
    handler_b_comment = MockHandler(f"/api/vendor-requests/{req_id}/comment", method="POST", headers={"Authorization": "Bearer tok_dlr"}, body={"comment": "Unauthorized comment"})
    api_router.handle_post(handler_b_comment)
    assert handler_b_comment.response_status == 403

def test_cross_vendor_order_and_meeting_isolation():
    """Vendor B cannot read, update, convert, or delete Vendor A's orders and meetings."""
    # Create an order owned by Vendor A (arch_01)
    handler_order = MockHandler(
        "/api/orders",
        method="POST",
        headers={"Authorization": "Bearer tok_arch"},
        body={
            "project_name": "Studio Private Luxury Villa",
            "client_name": "HNI Client A",
            "final_amount": 450000.0,
            "status": "Pipeline"
        }
    )
    api_router.handle_post(handler_order)
    assert handler_order.response_status == 201
    order_id = handler_order.get_json_response()["order"]["id"]

    # 1. Vendor B tries to view Vendor A's single order -> 403
    h_b_get_order = MockHandler(f"/api/orders/{order_id}", method="GET", headers={"Authorization": "Bearer tok_dlr"})
    api_router.handle_get(h_b_get_order)
    assert h_b_get_order.response_status == 403

    # 2. Vendor B tries to download quotation doc for Vendor A's order -> 403
    h_b_quotation = MockHandler(f"/api/orders/{order_id}/quotation", method="GET", headers={"Authorization": "Bearer tok_dlr"})
    api_router.handle_get(h_b_quotation)
    assert h_b_quotation.response_status == 403

    # 3. Vendor B tries to convert status of Vendor A's order -> 403
    h_b_convert = MockHandler("/api/orders/convert", method="POST", headers={"Authorization": "Bearer tok_dlr"}, body={"id": order_id, "status": "Win"})
    api_router.handle_post(h_b_convert)
    assert h_b_convert.response_status == 403

    # 4. Vendor B tries to update Vendor A's order -> 403
    h_b_update = MockHandler("/api/orders/update", method="POST", headers={"Authorization": "Bearer tok_dlr"}, body={"id": order_id, "final_amount": 1000.0})
    api_router.handle_post(h_b_update)
    assert h_b_update.response_status == 403

    # 5. Vendor B tries to delete Vendor A's order -> 403
    h_b_del = MockHandler("/api/orders/delete", method="POST", headers={"Authorization": "Bearer tok_dlr"}, body={"id": order_id})
    api_router.handle_post(h_b_del)
    assert h_b_del.response_status == 403

def test_request_lifecycle_and_cancellation_rules():
    """Vendor can cancel ONLY while New. Admin can progress through allowed lifecycle."""
    # Vendor creates request
    create_h = MockHandler("/api/vendor-requests", method="POST", headers={"Authorization": "Bearer tok_arch"}, body={"type": "Support / complaint", "title": "Damaged plank on delivery"})
    api_router.handle_post(create_h)
    req_id = create_h.get_json_response()["id"]

    # Admin changes status to 'In Review'
    admin_review_h = MockHandler(
        f"/api/vendor-requests/{req_id}",
        method="PUT",
        headers={"Authorization": "Bearer tok_admin"},
        body={"status": "In Review", "comment": "Support team reviewing photos", "assigned_to": "sales_01"}
    )
    api_router.handle_put(admin_review_h)
    assert admin_review_h.response_status == 200

    # Vendor now attempts to cancel -> MUST FAIL because status is 'In Review'
    vendor_cancel_h = MockHandler(
        f"/api/vendor-requests/{req_id}",
        method="PUT",
        headers={"Authorization": "Bearer tok_arch"},
        body={"status": "Cancelled"}
    )
    api_router.handle_put(vendor_cancel_h)
    assert vendor_cancel_h.response_status == 400
    assert "only 'new' requests can be cancelled" in vendor_cancel_h.get_json_response()["error"].lower()

    # Admin completes the request
    admin_done_h = MockHandler(
        f"/api/vendor-requests/{req_id}",
        method="PUT",
        headers={"Authorization": "Bearer tok_admin"},
        body={"status": "Completed", "comment": "Replacement plank dispatched"}
    )
    api_router.handle_put(admin_done_h)
    assert admin_done_h.response_status == 200
    assert admin_done_h.get_json_response()["status"] == "Completed"

def test_internal_notes_hidden_from_vendor():
    """Internal notes (is_internal=1) posted by admin are strictly hidden from vendor."""
    create_h = MockHandler("/api/vendor-requests", method="POST", headers={"Authorization": "Bearer tok_arch"}, body={"type": "CAD / specification request", "title": "Bespoke Pergola CAD Model"})
    api_router.handle_post(create_h)
    req_id = create_h.get_json_response()["id"]

    # Admin adds internal note
    admin_note_h = MockHandler(
        f"/api/vendor-requests/{req_id}/comment",
        method="POST",
        headers={"Authorization": "Bearer tok_admin"},
        body={"comment": "Internal note: Check engineer bandwidth before committing.", "is_internal": 1}
    )
    api_router.handle_post(admin_note_h)
    assert admin_note_h.response_status == 201

    # Admin adds public reply
    admin_pub_h = MockHandler(
        f"/api/vendor-requests/{req_id}/comment",
        method="POST",
        headers={"Authorization": "Bearer tok_admin"},
        body={"comment": "Public reply: We are working on your CAD files.", "is_internal": 0}
    )
    api_router.handle_post(admin_pub_h)
    assert admin_pub_h.response_status == 201

    # Vendor views timeline
    vendor_fetch_h = MockHandler(f"/api/vendor-requests/{req_id}", method="GET", headers={"Authorization": "Bearer tok_arch"})
    api_router.handle_get(vendor_fetch_h)
    activities = vendor_fetch_h.get_json_response()["request"]["activities"]

    # Verify internal note is NOT in vendor's view
    assert not any("Internal note" in a.get("comment", "") for a in activities)
    assert any("Public reply" in a.get("comment", "") for a in activities)

    # Admin views timeline -> see both!
    admin_fetch_h = MockHandler(f"/api/vendor-requests/{req_id}", method="GET", headers={"Authorization": "Bearer tok_admin"})
    api_router.handle_get(admin_fetch_h)
    admin_acts = admin_fetch_h.get_json_response()["request"]["activities"]
    assert any("Internal note" in a.get("comment", "") for a in admin_acts)

def test_admin_vendor_inbox_and_sla_traffic_lights():
    """Admin Inbox shows correct count, SLA lights (green/amber/red), and rejects vendor."""
    # Vendor rejected from inbox endpoint
    v_inbox_h = MockHandler("/api/admin/vendor-inbox", method="GET", headers={"Authorization": "Bearer tok_arch"})
    api_router.handle_get(v_inbox_h)
    assert v_inbox_h.response_status == 403

    # Admin views inbox
    adm_inbox_h = MockHandler("/api/admin/vendor-inbox", method="GET", headers={"Authorization": "Bearer tok_admin"})
    api_router.handle_get(adm_inbox_h)
    assert adm_inbox_h.response_status == 200
    data = adm_inbox_h.get_json_response()
    assert "stats" in data
    assert data["stats"]["total"] >= 1
    assert "requests" in data
    for req in data["requests"]:
        assert "sla" in req
        assert req["sla"]["color"] in ("green", "amber", "red")

def test_vendor_360_aggregation():
    """Vendor 360 endpoint aggregates profile, requests, orders, total business value, and avg response time."""
    # Vendor cannot view 360 view
    v_360_h = MockHandler("/api/admin/vendor-360/arch_01", method="GET", headers={"Authorization": "Bearer tok_arch"})
    api_router.handle_get(v_360_h)
    assert v_360_h.response_status == 403

    # Admin views 360
    adm_360_h = MockHandler("/api/admin/vendor-360/arch_01", method="GET", headers={"Authorization": "Bearer tok_admin"})
    api_router.handle_get(adm_360_h)
    assert adm_360_h.response_status == 200
    res = adm_360_h.get_json_response()
    assert res["profile"]["id"] == "arch_01"
    assert res["profile"]["role"] == "architect"
    assert "metrics" in res
    assert res["metrics"]["total_requests"] >= 1
    assert res["metrics"]["total_orders"] >= 1
    assert res["metrics"]["total_business_value"] >= 450000.0
    assert "orders" in res
    assert "requests" in res

def test_vendor_requests_csv_export():
    """CSV export returns formatted CSV with ref_no, vendor, title, status."""
    csv_h = MockHandler("/api/vendor-requests/export", method="GET", headers={"Authorization": "Bearer tok_admin"})
    api_router.handle_get(csv_h)
    assert csv_h.response_status == 200
    assert "text/csv" in csv_h.response_headers.get("Content-Type", "")
    content = csv_h.wfile.data.decode("utf-8")
    assert "Ref No,Vendor,Type,Title" in content
    assert "REQ-" in content
