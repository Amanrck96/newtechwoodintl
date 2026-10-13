"""REST API Router for NewTechWood CRM SQLite backend.

Phase 1 Security Fixes Applied:
  1. Passwords verified with bcrypt (not plain-text comparison)
  2. require_auth(roles) enforced on every protected endpoint
  3. password field stripped from ALL user/vendor responses
  4. /api/users and /api/vendors require admin/superadmin
  5. FY label unified; analytics year derived from financial_year param
  6. Pagination crash fixed (limit=0, negative page, no upper cap)
  7. Session cleanup on logout verified
"""
import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
import math

# Ensure db directory is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

import database

# ─── Password Hashing ─────────────────────────────────────────────────────────
try:
    import bcrypt
    def _hash_password(plain: str) -> str:
        return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    def _verify_password(plain: str, hashed: str) -> bool:
        try:
            if hashed.startswith('$2b$') or hashed.startswith('$2a$'):
                return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
            # Fallback: sha256 format from migrate.py
            if hashed.startswith('sha256$'):
                import hashlib
                _, salt, h = hashed.split('$')
                return hashlib.sha256((salt + plain).encode('utf-8')).hexdigest() == h
            return False
        except Exception:
            return False
    HASH_ALGO = 'bcrypt'
except ImportError:
    import hashlib, secrets as _secrets
    def _hash_password(plain: str) -> str:
        salt = _secrets.token_hex(16)
        h = hashlib.sha256((salt + plain).encode('utf-8')).hexdigest()
        return f"sha256${salt}${h}"
    def _verify_password(plain: str, hashed: str) -> bool:
        try:
            if hashed.startswith('sha256$'):
                _, salt, h = hashed.split('$')
                return hashlib.sha256((salt + plain).encode('utf-8')).hexdigest() == h
            return False
        except Exception:
            return False
    HASH_ALGO = 'sha256'

# ─── Role Hierarchy ───────────────────────────────────────────────────────────
# Higher index = more privileged
_ROLE_RANK = {'sales': 1, 'architect': 1, 'dealer': 1, 'admin': 2, 'superadmin': 3}

def _role_gte(user_role: str, required_role: str) -> bool:
    """Return True if user_role is at least as privileged as required_role."""
    return _ROLE_RANK.get(user_role, 0) >= _ROLE_RANK.get(required_role, 99)

# ─── Response Helpers ─────────────────────────────────────────────────────────
def send_json(handler, data, status=200):
    content = json.dumps(data, default=str).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(content)))
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    handler.end_headers()
    handler.wfile.write(content)
    try:
        handler.wfile.flush()
    except Exception:
        pass

def _safe_user(user: dict) -> dict:
    """Return user dict with password field stripped."""
    u = dict(user)
    u.pop('password', None)
    return u

# ─── Auth ─────────────────────────────────────────────────────────────────────
def get_auth_user(handler):
    """Resolve Bearer token → user dict (no password field). Returns None if invalid."""
    auth_header = handler.headers.get('Authorization', '')
    token = None
    if auth_header.startswith('Bearer '):
        token = auth_header[7:].strip()

    if not token:
        parsed = urlparse(handler.path)
        qs = parse_qs(parsed.query)
        token = qs.get('token', [None])[0]

    if not token:
        return None

    session = database.execute_one(
        "SELECT * FROM sessions WHERE token = ? AND expires_at > datetime('now');",
        (token,)
    )
    if not session:
        return None

    user = database.execute_one(
        "SELECT id, vendor_id, email, full_name, phone, role, status, permissions, avatar_initials, created_at "
        "FROM users WHERE id = ? AND status = 'active';",
        (session['user_id'],)
    )
    return user  # password NOT in SELECT list

def require_auth(handler, roles=None):
    """
    Enforce authentication and optional role check.
    roles: list of allowed roles e.g. ['admin','superadmin'], or None for any logged-in user.
    Returns user dict if authorized, else calls send_json with 401/403 and returns None.
    """
    user = get_auth_user(handler)
    if not user:
        send_json(handler, {"success": False, "error": "Unauthorized. Please log in."}, 401)
        return None
    if roles and user.get('role') not in roles:
        send_json(handler, {"success": False, "error": "Forbidden. Insufficient permissions."}, 403)
        return None
    return user

# ─── FY Helpers ───────────────────────────────────────────────────────────────
def _default_fy() -> str:
    """Return current financial year label in 'FY YY-YY' format."""
    now = datetime.now()
    if now.month >= 4:
        return f"FY {str(now.year)[2:]}-{str(now.year + 1)[2:]}"
    return f"FY {str(now.year - 1)[2:]}-{str(now.year)[2:]}"

def _fy_to_year_range(fy: str):
    """
    Parse 'FY 26-27' → (start_year=2026, end_year=2027).
    Handles both 2-digit and 4-digit year variants.
    """
    try:
        parts = fy.replace('FY', '').strip().split('-')
        y1 = int(parts[0].strip())
        y2 = int(parts[1].strip())
        if y1 < 100:
            base = 2000
            y1 += base
            y2 += base
        return y1, y2
    except Exception:
        now = datetime.now()
        return (now.year, now.year + 1) if now.month >= 4 else (now.year - 1, now.year)

def _month_to_year(month: int, fy: str) -> int:
    """Given a month number and FY string, return the actual calendar year for that month."""
    start_year, end_year = _fy_to_year_range(fy)
    # Apr(4)-Mar(3): Apr-Dec belong to start_year, Jan-Mar belong to end_year
    return start_year if month >= 4 else end_year

# ─── Main Handlers ────────────────────────────────────────────────────────────
def handle_get(handler):
    try:
        _handle_get_internal(handler)
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        send_json(handler, {"error": "Internal Server Error", "details": str(e)}, 500)

def _handle_get_internal(handler):
    parsed = urlparse(handler.path)
    path = parsed.path.rstrip('/')
    qs = parse_qs(parsed.query)

    # ── Public: Health Check ──────────────────────────────────────────────────
    if path == '/api/health':
        user_count = database.execute_one("SELECT COUNT(*) as count FROM users;")['count']
        project_count = database.execute_one("SELECT COUNT(*) as count FROM pipeline_projects;")['count']
        order_count = database.execute_one("SELECT COUNT(*) as count FROM waltz_orders;")['count']
        return send_json(handler, {
            "status": "ok",
            "database": "connected",
            "timestamp": datetime.now().isoformat(),
            "counts": {"users": user_count, "projects": project_count, "orders": order_count}
        })

    # ── Protected: Current Session User ──────────────────────────────────────
    if path == '/api/auth/me':
        user = get_auth_user(handler)
        if not user:
            return send_json(handler, {"success": False, "error": "Unauthorized or session expired"}, 401)
        return send_json(handler, {"success": True, "user": _safe_user(user)})

    # ── Protected (admin+): List Users / Vendors — password EXCLUDED ──────────
    if path in ('/api/users', '/api/vendors'):
        user = require_auth(handler, roles=['admin', 'superadmin'])
        if not user:
            return  # 401/403 already sent

        role_filter = qs.get('role', [''])[0].strip().lower()
        where_sql = ""
        params = []
        if role_filter and role_filter != 'all':
            where_sql = "WHERE lower(role) = ?"
            params = [role_filter]

        users = database.execute_query(f"""
            SELECT id, vendor_id, email, full_name, phone, role, status,
                   permissions, avatar_initials, created_at
            FROM users
            {where_sql}
            ORDER BY created_at ASC;
        """, tuple(params))
        user_list = [dict(u) for u in users]  # password NOT selected above
        return send_json(handler, {"success": True, "count": len(user_list), "vendors": user_list, "users": user_list})

    # ── Protected (any role): Dashboard ──────────────────────────────────────
    if path == '/api/dashboard':
        user = require_auth(handler)
        if not user:
            return

        default_fy = _default_fy()
        fy = qs.get('financial_year', [default_fy])[0].strip()
        months_param = qs.get('months', [''])[0].strip()
        chart_type = qs.get('chart_type', ['revenue'])[0].strip()

        selected_months = []
        if months_param:
            try:
                selected_months = [int(m.strip()) for m in months_param.split(',') if m.strip()]
            except Exception:
                selected_months = []

        where_clauses = []
        params = []
        if fy and fy.lower() != 'all':
            where_clauses.append("financial_year = ?")
            params.append(fy)
        if selected_months:
            placeholders = ','.join(['?'] * len(selected_months))
            where_clauses.append(f"month IN ({placeholders})")
            params.extend(selected_months)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        projects = database.execute_query(f"""
            SELECT id, project_name, client_name, location, city, state, country,
                   financial_year, month, day_bracket, category, total_value, sq_ft,
                   discount_pct, days_pipeline_to_win, stage, feedback_pending, feedback_notes,
                   coalesce(owner_name, 'Rohan Verma') as owner_name
            FROM pipeline_projects
            {where_sql}
            ORDER BY total_value DESC;
        """, tuple(params))

        feedback_pending_projects = [dict(p) for p in projects if p.get('feedback_pending') == 1]
        feedback_pending_count = len(feedback_pending_projects)

        pipeline_projects = [dict(p) for p in projects if p.get('stage') == 'Pipeline']
        win_projects = [dict(p) for p in projects if p.get('stage') == 'Win']

        pipeline_total_val = sum(float(p.get('total_value', 0)) for p in pipeline_projects)
        pipeline_count = len(pipeline_projects)
        pipeline_avg_discount = round(sum(float(p.get('discount_pct', 0)) for p in pipeline_projects) / pipeline_count, 1) if pipeline_count > 0 else 0.0

        win_total_val = sum(float(p.get('total_value', 0)) for p in win_projects)
        win_count = len(win_projects)
        win_avg_days = round(sum(int(p.get('days_pipeline_to_win', 0)) for p in win_projects) / win_count, 1) if win_count > 0 else 0.0
        win_avg_discount = round(sum(float(p.get('discount_pct', 0)) for p in win_projects) / win_count, 1) if win_count > 0 else 0.0

        brackets = ['1-5', '6-10', '11-15', '16-20', '21-25', '26-31']
        line_chart_win = [sum(1 for p in win_projects if p.get('day_bracket') == b) for b in brackets]
        line_chart_pipe = [sum(1 for p in pipeline_projects if p.get('day_bracket') == b) for b in brackets]

        fy_months = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]
        fy_month_labels = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
        bar_chart_pipeline_cr = []
        bar_chart_win_cr = []
        for m in fy_months:
            p_sum = sum(float(p.get('total_value', 0)) for p in pipeline_projects if p.get('month') == m)
            w_sum = sum(float(p.get('total_value', 0)) for p in win_projects if p.get('month') == m)
            bar_chart_pipeline_cr.append(round(p_sum / 10_000_000.0, 2))
            bar_chart_win_cr.append(round(w_sum / 10_000_000.0, 2))

        categories = sorted(list(set(p.get('category', 'Other') for p in projects if p.get('category'))))
        product_breakdown = []
        for cat in categories:
            cat_p = [p for p in projects if p.get('category') == cat]
            product_breakdown.append({
                "category": cat,
                "amount": sum(float(p.get('total_value', 0)) for p in cat_p),
                "amount_cr": round(sum(float(p.get('total_value', 0)) for p in cat_p) / 10_000_000.0, 2),
                "sq_ft": sum(float(p.get('sq_ft', 0)) for p in cat_p),
                "count": len(cat_p)
            })

        traffic_light_items = []
        for p in projects:
            p_dict = dict(p)
            disc = float(p_dict.get('discount_pct', 0))
            is_fb = bool(p_dict.get('feedback_pending', 0))
            stg = p_dict.get('stage')
            if is_fb:
                light, reason = 'red', f'Feedback Pending ({p_dict.get("feedback_notes") or "Awaiting client response"})'
            elif disc > 12.0 and stg == 'Pipeline':
                light, reason = 'amber', f'High Discount Requested ({disc}%)'
            elif stg == 'Pipeline':
                light, reason = 'amber', 'Active Negotiation / BOQ Review'
            elif stg == 'Win':
                light, reason = 'green', f'Won & Invoiced ({p_dict.get("days_pipeline_to_win", 0)} days)'
            else:
                light, reason = 'red', 'Lost Deal'
            p_dict['traffic_light'] = light
            p_dict['traffic_reason'] = reason
            traffic_light_items.append(p_dict)

        all_fys = database.execute_query("SELECT DISTINCT financial_year FROM pipeline_projects ORDER BY financial_year DESC;")
        distinct_fys = [row['financial_year'] for row in all_fys if row.get('financial_year')]

        return send_json(handler, {
            "success": True,
            "filters": {"financial_year": fy, "months": selected_months, "chart_type": chart_type},
            "available_fys": distinct_fys,
            "alert": {"feedback_pending_count": feedback_pending_count, "feedback_pending_projects": feedback_pending_projects},
            "kpis": {
                "pipeline": {"total_value": pipeline_total_val, "count": pipeline_count, "avg_discount": pipeline_avg_discount},
                "win": {"total_value": win_total_val, "count": win_count, "avg_days": win_avg_days, "avg_discount": win_avg_discount}
            },
            "charts": {
                "line_chart": {"labels": brackets, "win_series": line_chart_win, "pipeline_series": line_chart_pipe},
                "bar_chart": {"months": fy_month_labels, "month_nums": fy_months, "pipeline_cr": bar_chart_pipeline_cr, "win_cr": bar_chart_win_cr},
                "product_breakdown": product_breakdown
            },
            "traffic_light": traffic_light_items,
            "top_10_pipeline": pipeline_projects[:10],
            "all_projects_count": len(projects)
        })

    # ── Protected (any role): Analytics ──────────────────────────────────────
    if path == '/api/analytics':
        user = require_auth(handler)
        if not user:
            return

        from_date = qs.get('from_date', [''])[0].strip()
        to_date = qs.get('to_date', [''])[0].strip()
        user_filter = qs.get('user', ['all'])[0].strip()
        status_filter = qs.get('status', ['all'])[0].strip()
        # FY param used to correctly derive calendar year for pipeline projects
        fy = qs.get('financial_year', [_default_fy()])[0].strip()

        orders = database.execute_query("""
            SELECT id, order_number as ref_no, project_name as title, client_name as client,
                   city, state, order_date as activity_date, status, final_amount as amount,
                   source, coalesce(owner_name, 'Rohan Verma') as owner_name, 'Material Order' as activity_type
            FROM waltz_orders;
        """)

        projects = database.execute_query("""
            SELECT id, id as ref_no, project_name as title, client_name as client,
                   city, state, financial_year, month, day_bracket, stage as status,
                   total_value as amount, category as source, coalesce(owner_name, 'Rohan Verma') as owner_name,
                   'Pipeline Project' as activity_type
            FROM pipeline_projects;
        """)

        meetings = database.execute_query("""
            SELECT id, id as ref_no, firm_name as title, guest_name as client,
                   city, state, meeting_date as activity_date, 'Meeting' as status,
                   0.0 as amount, guest_type as source, coalesce(owner_name, 'Rohan Verma') as owner_name,
                   'Architect Meeting' as activity_type
            FROM meetings;
        """)

        # Normalize pipeline project dates using FY-aware year calculation
        bracket_days = {'1-5': '03', '6-10': '08', '11-15': '13', '16-20': '18', '21-25': '23', '26-31': '28'}
        normalized_projects = []
        for p in projects:
            p_dict = dict(p)
            m = p_dict.get('month', 10)
            # Use FY from the project's own financial_year field if available, else param
            proj_fy = p_dict.get('financial_year') or fy
            year = _month_to_year(m, proj_fy)
            b = p_dict.get('day_bracket', '1-5')
            day = bracket_days.get(b, '15')
            p_dict['activity_date'] = f"{year}-{m:02d}-{day}"
            normalized_projects.append(p_dict)

        all_activities = [dict(o) for o in orders] + normalized_projects + [dict(m) for m in meetings]

        distinct_users = sorted(list(set(a['owner_name'] for a in all_activities if a.get('owner_name'))))

        filtered = []
        for a in all_activities:
            act_date = a.get('activity_date', '')
            if from_date and act_date < from_date:
                continue
            if to_date and act_date > to_date:
                continue
            if user_filter and user_filter.lower() != 'all' and a.get('owner_name', '').lower() != user_filter.lower():
                continue
            if status_filter and status_filter.lower() != 'all':
                s = a.get('status', '')
                if status_filter.lower() == 'win' and s not in ('Win',):
                    continue
                elif status_filter.lower() == 'pipeline' and s != 'Pipeline':
                    continue
                elif status_filter.lower() == 'lost' and s != 'Lost':
                    continue
                elif status_filter.lower() == 'meeting' and a.get('activity_type') != 'Architect Meeting':
                    continue
            filtered.append(a)

        filtered.sort(key=lambda x: x.get('activity_date', ''), reverse=True)

        total_revenue = sum(float(x.get('amount', 0)) for x in filtered if x.get('status') == 'Win')
        total_pipeline = sum(float(x.get('amount', 0)) for x in filtered if x.get('status') == 'Pipeline')
        total_lost = sum(float(x.get('amount', 0)) for x in filtered if x.get('status') == 'Lost')

        # Win rate: only count Pipeline Projects + Material Orders (not meetings, they have no amount)
        won_count = sum(1 for x in filtered if x.get('status') == 'Win' and x.get('activity_type') != 'Architect Meeting')
        lost_count = sum(1 for x in filtered if x.get('status') == 'Lost' and x.get('activity_type') != 'Architect Meeting')
        pipeline_count = sum(1 for x in filtered if x.get('status') == 'Pipeline')
        meetings_count = sum(1 for x in filtered if x.get('activity_type') == 'Architect Meeting')

        closed_total = won_count + lost_count
        win_rate = round((won_count / closed_total * 100), 1) if closed_total > 0 else 0.0
        avg_deal_size = round(total_revenue / won_count, 0) if won_count > 0 else 0.0

        return send_json(handler, {
            "success": True,
            "filters": {"from_date": from_date, "to_date": to_date, "user": user_filter, "status": status_filter},
            "metrics": {
                "total_activities": len(filtered),
                "total_revenue": total_revenue,
                "total_pipeline": total_pipeline,
                "total_lost": total_lost,
                "won_count": won_count,
                "pipeline_count": pipeline_count,
                "lost_count": lost_count,
                "meetings_count": meetings_count,
                "win_rate_pct": win_rate,
                "avg_deal_size": avg_deal_size
            },
            "distinct_users": distinct_users,
            "activities": filtered
        })

    # ── Protected (any role): Directory Firms (N+1 kept; min-3-letter enforced) ─
    if path == '/api/directory/firms':
        user = require_auth(handler)
        if not user:
            return

        search = qs.get('search', [''])[0].strip().lower()
        category = qs.get('category', ['all'])[0].strip()

        # Enforce min 3 characters for search (JB Glass rule)
        if search and len(search) < 3:
            return send_json(handler, {"success": True, "count": 0, "firms": [],
                                       "note": "Search requires at least 3 characters"})

        where_clauses = []
        params = []
        if category and category.lower() != 'all':
            where_clauses.append("category = ?")
            params.append(category)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        firms = database.execute_query(f"""
            SELECT id, firm_name, category, city, state, country, status
            FROM directory_firms
            {where_sql}
            ORDER BY firm_name ASC;
        """, tuple(params))

        result = []
        for firm in firms:
            f_dict = dict(firm)
            contacts = database.execute_query("""
                SELECT id, firm_id, first_name, last_name, user_type, mobile, email, is_primary
                FROM directory_contacts
                WHERE firm_id = ?
                ORDER BY is_primary DESC, first_name ASC;
            """, (f_dict['id'],))
            f_dict['contacts'] = [dict(c) for c in contacts]

            if search:
                term = search
                match = (term in f_dict['firm_name'].lower() or
                         term in (f_dict.get('city') or '').lower() or
                         term in (f_dict.get('state') or '').lower() or
                         any(term in (c.get('first_name') or '').lower() or
                             term in (c.get('last_name') or '').lower() or
                             term in (c.get('email') or '').lower() or
                             term in (c.get('mobile') or '') for c in f_dict['contacts']))
                if not match:
                    continue
            result.append(f_dict)

        return send_json(handler, {"success": True, "count": len(result), "firms": result})

    # ── Protected (any role): Meetings ───────────────────────────────────────
    if path == '/api/directory/meetings':
        user = require_auth(handler)
        if not user:
            return

        from_date = qs.get('from_date', [''])[0].strip()
        to_date = qs.get('to_date', [''])[0].strip()
        firm_name = qs.get('firm_name', [''])[0].strip().lower()
        guest_name = qs.get('guest_name', [''])[0].strip().lower()
        mobile = qs.get('mobile', [''])[0].strip()
        user_type = qs.get('user_type', [''])[0].strip()
        guest_type = qs.get('guest_type', [''])[0].strip()
        country = qs.get('country', [''])[0].strip()
        state = qs.get('state', [''])[0].strip()
        city = qs.get('city', [''])[0].strip()

        where_clauses = []
        params = []
        if from_date:
            where_clauses.append("meeting_date >= ?"); params.append(from_date)
        if to_date:
            where_clauses.append("meeting_date <= ?"); params.append(to_date)
        if firm_name:
            where_clauses.append("lower(firm_name) LIKE ?"); params.append(f"%{firm_name}%")
        if guest_name:
            where_clauses.append("lower(guest_name) LIKE ?"); params.append(f"%{guest_name}%")
        if mobile:
            where_clauses.append("mobile LIKE ?"); params.append(f"%{mobile}%")
        if user_type and user_type.lower() != 'all':
            where_clauses.append("user_type = ?"); params.append(user_type)
        if guest_type and guest_type.lower() != 'all':
            where_clauses.append("guest_type = ?"); params.append(guest_type)
        if country and country.lower() != 'all':
            where_clauses.append("country = ?"); params.append(country)
        if state and state.lower() != 'all':
            where_clauses.append("state = ?"); params.append(state)
        if city and city.lower() != 'all':
            where_clauses.append("city = ?"); params.append(city)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        meetings = database.execute_query(f"""
            SELECT id, meeting_date, firm_name, guest_name, mobile, user_type,
                   guest_type, country, state, city, status, discussion_notes, image_urls,
                   coalesce(owner_name, 'Rohan Verma') as owner_name
            FROM meetings
            {where_sql}
            ORDER BY meeting_date DESC;
        """, tuple(params))
        return send_json(handler, {"success": True, "count": len(meetings), "meetings": [dict(m) for m in meetings]})

    # ── Protected (any role): Invitations ────────────────────────────────────
    if path == '/api/directory/invitations':
        user = require_auth(handler)
        if not user:
            return

        invitations = database.execute_query("""
            SELECT id, invitation_code, recipient_name, firm_name, recipient_email,
                   mobile, invitation_link, status, created_at, expires_at
            FROM id_invitations
            ORDER BY created_at DESC;
        """)
        return send_json(handler, {"success": True, "count": len(invitations), "invitations": [dict(i) for i in invitations]})

    # ── Protected (any role): Visitors — pagination crash fixed ──────────────
    if path == '/api/directory/visitors':
        user = require_auth(handler)
        if not user:
            return

        try:
            page = max(1, int(qs.get('page', ['1'])[0]))
        except Exception:
            page = 1
        try:
            limit = max(1, min(200, int(qs.get('limit', ['25'])[0])))  # clamp 1..200
        except Exception:
            limit = 25

        visitor_type = qs.get('visitor_type', [''])[0].strip()
        name = qs.get('name', [''])[0].strip().lower()
        mobile = qs.get('mobile', [''])[0].strip()
        email = qs.get('email', [''])[0].strip().lower()
        firm = qs.get('firm', [''])[0].strip().lower()
        from_created = qs.get('from_created_date', [''])[0].strip()
        to_created = qs.get('to_created_date', [''])[0].strip()
        country = qs.get('country', [''])[0].strip()
        state = qs.get('state', [''])[0].strip()
        city = qs.get('city', [''])[0].strip()
        event_year = qs.get('event_year', [''])[0].strip()

        where_clauses = []
        params = []
        if visitor_type and visitor_type.lower() != 'all':
            where_clauses.append("visitor_type = ?"); params.append(visitor_type)
        if name:
            where_clauses.append("lower(name) LIKE ?"); params.append(f"%{name}%")
        if mobile:
            where_clauses.append("mobile LIKE ?"); params.append(f"%{mobile}%")
        if email:
            where_clauses.append("lower(email) LIKE ?"); params.append(f"%{email}%")
        if firm:
            where_clauses.append("lower(firm) LIKE ?"); params.append(f"%{firm}%")
        if from_created:
            where_clauses.append("link_created_date >= ?"); params.append(from_created)
        if to_created:
            where_clauses.append("link_created_date <= ?"); params.append(to_created)
        if country and country.lower() != 'all':
            where_clauses.append("country = ?"); params.append(country)
        if state and state.lower() != 'all':
            where_clauses.append("state = ?"); params.append(state)
        if city and city.lower() != 'all':
            where_clauses.append("city = ?"); params.append(city)
        if event_year and event_year.lower() != 'all':
            where_clauses.append("event_year = ?"); params.append(event_year)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        total_row = database.execute_one(f"SELECT COUNT(*) as count FROM id_visitors {where_sql};", tuple(params))
        total_count = total_row['count'] if total_row else 0
        total_pages = max(1, math.ceil(total_count / limit))
        page = min(page, total_pages)  # clamp to valid range
        offset = (page - 1) * limit

        visitors = database.execute_query(f"""
            SELECT id, visitor_type, name, mobile, email, firm,
                   link_created_date, form_submitted_date, country, state, city, event_year, created_at
            FROM id_visitors
            {where_sql}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?;
        """, tuple(params + [limit, offset]))

        return send_json(handler, {
            "success": True, "total": total_count, "page": page,
            "limit": limit, "total_pages": total_pages,
            "visitors": [dict(v) for v in visitors]
        })

    # ── Protected (any role): Go Pro Assets ──────────────────────────────────
    if path == '/api/gopro/assets':
        user = require_auth(handler)
        if not user:
            return

        subject = qs.get('subject', [''])[0].strip().lower()
        creator = qs.get('creator', [''])[0].strip().lower()
        file_type = qs.get('file_type', [''])[0].strip()

        where_clauses = []
        params = []
        if subject:
            where_clauses.append("lower(subject) LIKE ?"); params.append(f"%{subject}%")
        if creator:
            where_clauses.append("lower(creator) LIKE ?"); params.append(f"%{creator}%")
        if file_type and file_type.lower() != 'all':
            where_clauses.append("file_type = ?"); params.append(file_type)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        assets = database.execute_query(f"""
            SELECT id, subject, creator, file_type, duration, video_url, thumbnail_url, category, views_count
            FROM go_pro_assets
            {where_sql}
            ORDER BY id ASC;
        """, tuple(params))
        return send_json(handler, {"success": True, "count": len(assets), "assets": [dict(a) for a in assets]})

    # ── Protected (any role): Orders List ────────────────────────────────────
    if path == '/api/orders':
        user = require_auth(handler)
        if not user:
            return

        order_number = qs.get('order_number', [''])[0].strip().lower()
        project_name = qs.get('project_name', [''])[0].strip().lower()
        client_name = qs.get('client_name', [''])[0].strip().lower()
        country = qs.get('country', [''])[0].strip()
        state = qs.get('state', [''])[0].strip()
        city = qs.get('city', [''])[0].strip()
        from_date = qs.get('from_date', [''])[0].strip()
        to_date = qs.get('to_date', [''])[0].strip()
        status_filter = qs.get('status', [''])[0].strip()
        source = qs.get('source', [''])[0].strip()

        where_clauses = []
        params = []
        if order_number:
            where_clauses.append("lower(order_number) LIKE ?"); params.append(f"%{order_number}%")
        if project_name:
            where_clauses.append("lower(project_name) LIKE ?"); params.append(f"%{project_name}%")
        if client_name:
            where_clauses.append("lower(client_name) LIKE ?"); params.append(f"%{client_name}%")
        if country and country.lower() != 'all':
            where_clauses.append("country = ?"); params.append(country)
        if state and state.lower() != 'all':
            where_clauses.append("state = ?"); params.append(state)
        if city and city.lower() != 'all':
            where_clauses.append("city = ?"); params.append(city)
        if from_date:
            where_clauses.append("order_date >= ?"); params.append(from_date)
        if to_date:
            where_clauses.append("order_date <= ?"); params.append(to_date)
        if status_filter and status_filter.lower() != 'all':
            where_clauses.append("status = ?"); params.append(status_filter)
        if source and source.lower() != 'all':
            where_clauses.append("source = ?"); params.append(source)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        orders = database.execute_query(f"""
            SELECT id, order_number, project_name, client_name, country, state, city,
                   order_date, status, final_amount, source, notes,
                   coalesce(owner_name, 'Rohan Verma') as owner_name, created_at
            FROM waltz_orders
            {where_sql}
            ORDER BY order_date DESC;
        """, tuple(params))
        return send_json(handler, {"success": True, "count": len(orders), "orders": [dict(o) for o in orders]})

    # ── Protected (any role): Pipeline Projects List / Single Project ────────
    if path == '/api/projects' or path.startswith('/api/projects/'):
        user = require_auth(handler)
        if not user:
            return

        if path.startswith('/api/projects/') and path != '/api/projects':
            proj_id = path.split('/')[-1]
            proj = database.execute_one("SELECT * FROM pipeline_projects WHERE id = ?;", (proj_id,))
            if not proj:
                return send_json(handler, {"success": False, "error": "Project not found"}, 404)
            return send_json(handler, {"success": True, "project": dict(proj)})

        stage_filter = qs.get('stage', [''])[0].strip()
        fy_filter = qs.get('financial_year', [''])[0].strip()
        month_filter = qs.get('month', [''])[0].strip()
        search = qs.get('search', [''])[0].strip().lower()
        feedback_pending = qs.get('feedback_pending', [''])[0].strip()

        where_clauses = []
        params = []
        if stage_filter and stage_filter.lower() != 'all':
            where_clauses.append("stage = ?"); params.append(stage_filter)
        if fy_filter and fy_filter.lower() != 'all':
            where_clauses.append("financial_year = ?"); params.append(fy_filter)
        if month_filter and month_filter.lower() != 'all':
            try:
                where_clauses.append("month = ?"); params.append(int(month_filter))
            except Exception:
                pass
        if feedback_pending in ('1', 'true', 'True'):
            where_clauses.append("feedback_pending = 1")
        elif feedback_pending in ('0', 'false', 'False'):
            where_clauses.append("feedback_pending = 0")
        if search:
            where_clauses.append("(lower(project_name) LIKE ? OR lower(client_name) LIKE ? OR lower(city) LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        projects = database.execute_query(f"""
            SELECT * FROM pipeline_projects
            {where_sql}
            ORDER BY created_at DESC;
        """, tuple(params))
        return send_json(handler, {"success": True, "count": len(projects), "projects": [dict(p) for p in projects]})

    send_json(handler, {"error": "Endpoint not found", "path": path}, 404)


# ─── POST Handler ─────────────────────────────────────────────────────────────
def handle_post(handler):
    try:
        _handle_post_internal(handler)
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        send_json(handler, {"error": "Internal Server Error", "details": str(e)}, 500)

def _handle_post_internal(handler):
    parsed = urlparse(handler.path)
    path = parsed.path.rstrip('/')

    content_length = int(handler.headers.get('Content-Length', 0))
    body_bytes = handler.rfile.read(content_length) if content_length > 0 else b'{}'
    try:
        body = json.loads(body_bytes.decode('utf-8'))
    except Exception:
        body = {}

    # ── Public: Login ─────────────────────────────────────────────────────────
    if path == '/api/auth/login':
        email = (body.get('email') or '').strip().lower()
        password = (body.get('password') or '').strip()
        remember = bool(body.get('remember', False))

        if not email or not password:
            return send_json(handler, {"success": False, "error": "Email and password are required"}, 400)

        user = database.execute_one(
            "SELECT * FROM users WHERE (lower(email) = ? OR lower(id) = ? OR lower(COALESCE(vendor_id, '')) = ?) AND status = 'active';",
            (email, email, email)
        )

        if not user:
            return send_json(handler, {"success": False, "error": "Invalid username or password"}, 401)

        # Secure password verification — bcrypt or sha256 hash
        stored_pw = user.get('password', '')
        if not _verify_password(password, stored_pw):
            return send_json(handler, {"success": False, "error": "Invalid username or password"}, 401)

        token = 'ntw_' + uuid.uuid4().hex
        expires_days = 30 if remember else 1
        expires_at = (datetime.now() + timedelta(days=expires_days)).strftime("%Y-%m-%d %H:%M:%S")

        database.execute_commit(
            "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?);",
            (token, user['id'], expires_at)
        )

        safe_user = {
            "id": user['id'],
            "vendor_id": user.get('vendor_id') or user['id'],
            "email": user['email'],
            "full_name": user['full_name'],
            "role": user['role'],
            "status": user['status'],
            "phone": user.get('phone', ''),
            "permissions": user.get('permissions', ''),
            "avatar_initials": user.get('avatar_initials') or user['full_name'][:2].upper()
        }

        return send_json(handler, {
            "success": True,
            "token": token,
            "expires_at": expires_at,
            "user": safe_user
        })

    # ── Protected: Logout ─────────────────────────────────────────────────────
    if path == '/api/auth/logout':
        auth_header = handler.headers.get('Authorization', '')
        token = auth_header[7:].strip() if auth_header.startswith('Bearer ') else body.get('token')
        if token:
            database.execute_commit("DELETE FROM sessions WHERE token = ?;", (token,))
        return send_json(handler, {"success": True, "message": "Logged out successfully"})

    # ── Protected (admin+): Create Vendor ────────────────────────────────────
    if path in ('/api/vendors', '/api/users'):
        auth_user = require_auth(handler, roles=['admin', 'superadmin'])
        if not auth_user:
            return

        firm_name = (body.get('firm_name') or body.get('name') or body.get('full_name') or '').strip()
        email = (body.get('email') or '').strip().lower()
        password = (body.get('password') or '').strip()
        role = (body.get('role') or 'architect').strip().lower()
        vendor_id = (body.get('vendor_id') or body.get('vendorId') or '').strip()
        phone = (body.get('phone') or '').strip()
        status = (body.get('status') or 'active').strip().lower()
        permissions = body.get('permissions')
        if isinstance(permissions, list):
            permissions = ','.join(permissions)
        elif not permissions:
            if role in ('admin', 'superadmin'):
                permissions = 'all'
            elif role == 'architect':
                permissions = 'gopro_cad,pipeline_specs,meetings,invitations'
            elif role == 'dealer':
                permissions = 'waltz_orders,wholesale_catalog,invitations'
            else:
                permissions = 'pipeline,orders,meetings,visitors'

        if not firm_name or not email or not password:
            return send_json(handler, {"success": False, "error": "Firm name, email, and password are required"}, 400)

        existing_email = database.execute_one("SELECT id FROM users WHERE lower(email) = ?;", (email,))
        if existing_email:
            return send_json(handler, {"success": False, "error": f"An account with email '{email}' already exists"}, 409)

        if not vendor_id:
            prefix = {'architect': 'VND', 'dealer': 'DLR', 'sales': 'SAL'}.get(role, 'ADM')
            vendor_id = f"{prefix}-2026-{uuid.uuid4().hex[:4].upper()}"

        existing_vid = database.execute_one("SELECT id FROM users WHERE lower(vendor_id) = ?;", (vendor_id.lower(),))
        if existing_vid:
            vendor_id = f"{vendor_id}-{uuid.uuid4().hex[:3].upper()}"

        user_id = f"vnd_{uuid.uuid4().hex[:8]}"
        initials = ''.join([w[0] for w in firm_name.split() if w])[:2].upper() or 'VN'
        hashed_pw = _hash_password(password)  # HASH before storing

        database.execute_commit("""
            INSERT INTO users (id, vendor_id, email, password, full_name, phone, role, status, permissions, avatar_initials)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (user_id, vendor_id, email, hashed_pw, firm_name, phone, role, status, permissions, initials))

        created = database.execute_one("""
            SELECT id, vendor_id, email, full_name, phone, role, status, permissions, avatar_initials, created_at
            FROM users WHERE id = ?;
        """, (user_id,))  # password NOT selected
        return send_json(handler, {"success": True, "message": "Vendor account created successfully", "vendor": dict(created)}, 201)

    # ── Protected (admin+): Vendor status toggle ──────────────────────────────
    if path in ('/api/vendors/status', '/api/vendors/toggle-status'):
        auth_user = require_auth(handler, roles=['admin', 'superadmin'])
        if not auth_user:
            return

        user_id = body.get('id') or body.get('vendor_id')
        new_status = body.get('status')
        if not user_id:
            return send_json(handler, {"success": False, "error": "Vendor ID required"}, 400)

        curr = database.execute_one("SELECT id, role, status FROM users WHERE id = ? OR vendor_id = ?;", (user_id, user_id))
        if not curr:
            return send_json(handler, {"success": False, "error": "Vendor not found"}, 404)

        if not new_status:
            new_status = 'inactive' if curr['status'] == 'active' else 'active'

        database.execute_commit("UPDATE users SET status = ? WHERE id = ?;", (new_status, curr['id']))
        return send_json(handler, {"success": True, "message": f"Status updated to {new_status}", "id": curr['id'], "status": new_status})

    # ── Protected (admin+): Update Vendor ────────────────────────────────────
    if path == '/api/vendors/update':
        auth_user = require_auth(handler, roles=['admin', 'superadmin'])
        if not auth_user:
            return

        user_id = body.get('id') or body.get('vendor_id')
        if not user_id:
            return send_json(handler, {"success": False, "error": "Vendor ID required"}, 400)

        curr = database.execute_one("SELECT * FROM users WHERE id = ? OR vendor_id = ?;", (user_id, user_id))
        if not curr:
            return send_json(handler, {"success": False, "error": "Vendor not found"}, 404)

        full_name = body.get('firm_name') or body.get('name') or body.get('full_name') or curr['full_name']
        email = body.get('email') or curr['email']
        role = body.get('role') or curr['role']
        status = body.get('status') or curr['status']
        phone = body.get('phone') or curr['phone']
        permissions = body.get('permissions')
        if isinstance(permissions, list):
            permissions = ','.join(permissions)
        elif permissions is None:
            permissions = curr['permissions']

        # Only re-hash if a new plaintext password was provided
        new_plain_pw = body.get('password', '').strip()
        if new_plain_pw:
            stored_pw = _hash_password(new_plain_pw)
        else:
            stored_pw = curr['password']  # keep existing hash

        database.execute_commit("""
            UPDATE users
            SET full_name = ?, email = ?, password = ?, role = ?, status = ?, phone = ?, permissions = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?;
        """, (full_name, email, stored_pw, role, status, phone, permissions, curr['id']))

        updated = database.execute_one("""
            SELECT id, vendor_id, email, full_name, phone, role, status, permissions, avatar_initials, created_at
            FROM users WHERE id = ?;
        """, (curr['id'],))  # password NOT selected
        return send_json(handler, {"success": True, "message": "Vendor updated successfully", "vendor": dict(updated)})

    # ── Protected (admin+): Delete Vendor (POST fallback) ────────────────────
    if path == '/api/vendors/delete':
        auth_user = require_auth(handler, roles=['admin', 'superadmin'])
        if not auth_user:
            return

        user_id = body.get('id') or body.get('vendor_id')
        if not user_id:
            return send_json(handler, {"success": False, "error": "Vendor ID required"}, 400)

        curr = database.execute_one("SELECT id, role FROM users WHERE id = ? OR vendor_id = ?;", (user_id, user_id))
        if not curr:
            return send_json(handler, {"success": False, "error": "Vendor not found"}, 404)

        if curr['id'] == 'admin' or curr['role'] == 'superadmin':
            return send_json(handler, {"success": False, "error": "Cannot delete root Super Administrator account"}, 403)

        database.execute_commit("DELETE FROM sessions WHERE user_id = ?;", (curr['id'],))
        database.execute_commit("DELETE FROM users WHERE id = ?;", (curr['id'],))
        return send_json(handler, {"success": True, "message": "Vendor deleted successfully", "id": curr['id']})

    # ── Protected (any role): Create Order ───────────────────────────────────
    if path == '/api/orders':
        auth_user = require_auth(handler)
        if not auth_user:
            return

        proj_name = body.get('project_name', '').strip()
        client_name = body.get('client_name', '').strip()
        order_num = body.get('order_number', '').strip()
        if not order_num:
            order_num = f"NTW-{datetime.now().year}-{uuid.uuid4().hex[:6].upper()}"
        if not proj_name or not client_name:
            return send_json(handler, {"success": False, "error": "Project and client name are required"}, 400)

        order_id = f"ORD-NTW-{uuid.uuid4().hex[:8]}"
        country = body.get('country', 'India')
        state = body.get('state', 'Karnataka')          # default changed to Karnataka
        city = body.get('city', 'Bengaluru')            # default changed to Bengaluru
        order_date = body.get('order_date') or datetime.now().strftime("%Y-%m-%d")
        status = body.get('status', 'Pipeline')
        try:
            final_amount = float(body.get('final_amount', 0.0))
        except Exception:
            final_amount = 0.0
        source = body.get('source', 'Direct Architect')
        notes = body.get('notes', '')
        owner_name = body.get('owner_name') or auth_user.get('full_name', 'Rohan Verma')

        database.execute_commit("""
            INSERT INTO waltz_orders (id, order_number, project_name, client_name, country, state, city,
                                      order_date, status, final_amount, source, notes, owner_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (order_id, order_num, proj_name, client_name, country, state, city, order_date, status, final_amount, source, notes, owner_name))

        created = database.execute_one("SELECT * FROM waltz_orders WHERE id = ?;", (order_id,))
        return send_json(handler, {"success": True, "message": "Order created successfully", "order": dict(created)}, 201)

    # ── Protected (any role): Update Order (POST fallback) ───────────────────
    if path == '/api/orders/update':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        return _update_order_internal(handler, body)

    # ── Protected (any role): Delete Order (POST fallback) ───────────────────
    if path == '/api/orders/delete':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        order_id = body.get('id')
        if not order_id:
            return send_json(handler, {"success": False, "error": "Order ID is required"}, 400)
        database.execute_commit("DELETE FROM waltz_orders WHERE id = ?;", (order_id,))
        return send_json(handler, {"success": True, "message": "Order deleted successfully"})

    # ── Protected (any role): Create Invitation ───────────────────────────────
    if path == '/api/directory/invitations':
        auth_user = require_auth(handler)
        if not auth_user:
            return

        recip_name = body.get('recipient_name', '').strip()
        firm_name = body.get('firm_name', '').strip()
        email = body.get('recipient_email', '').strip()
        mobile = body.get('mobile', '').strip()
        if not recip_name or not firm_name:
            return send_json(handler, {"success": False, "error": "Recipient name and firm name required"}, 400)

        inv_code = f"NTW-INV-{uuid.uuid4().hex[:6].upper()}"
        inv_link = f"https://newtechwood.in/invite/{inv_code}"
        inv_id = body.get('id') or f"INV-{uuid.uuid4().hex[:8]}"
        expires_at = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

        database.execute_commit("""
            INSERT INTO id_invitations (id, invitation_code, recipient_name, firm_name, recipient_email,
                                        mobile, invitation_link, status, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Active', ?);
        """, (inv_id, inv_code, recip_name, firm_name, email, mobile, inv_link, expires_at))

        created = database.execute_one("SELECT * FROM id_invitations WHERE id = ?;", (inv_id,))
        return send_json(handler, {"success": True, "message": "Invitation generated", "invitation": dict(created)}, 201)

    # ── Protected (any role): Create Meeting ─────────────────────────────────
    if path == '/api/directory/meetings':
        auth_user = require_auth(handler)
        if not auth_user:
            return

        firm = body.get('firm_name', '').strip()
        guest = body.get('guest_name', '').strip()
        if not firm or not guest:
            return send_json(handler, {"success": False, "error": "Firm and guest names required"}, 400)

        mtg_id = body.get('id') or f"MTG-{uuid.uuid4().hex[:8]}"
        mtg_date = body.get('meeting_date') or datetime.now().strftime("%Y-%m-%d")
        mobile = body.get('mobile', '')
        user_type = body.get('user_type', 'New')
        guest_type = body.get('guest_type', 'Architect')
        country = body.get('country', 'India')
        state = body.get('state', 'Karnataka')
        city = body.get('city', 'Bengaluru')
        notes = body.get('discussion_notes', '')
        owner_name = body.get('owner_name') or auth_user.get('full_name', 'Rohan Verma')

        database.execute_commit("""
            INSERT INTO meetings (id, meeting_date, firm_name, guest_name, mobile, user_type, guest_type,
                                  country, state, city, status, discussion_notes, image_urls, owner_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Completed', ?, '[]', ?);
        """, (mtg_id, mtg_date, firm, guest, mobile, user_type, guest_type, country, state, city, notes, owner_name))

        created = database.execute_one("SELECT * FROM meetings WHERE id = ?;", (mtg_id,))
        return send_json(handler, {"success": True, "message": "Meeting scheduled", "meeting": dict(created)}, 201)

    # ── Protected: Create Pipeline Project ───────────────────────────────────
    if path == '/api/projects':
        auth_user = require_auth(handler)
        if not auth_user:
            return

        proj_name = body.get('project_name', '').strip()
        client_name = body.get('client_name', '').strip()
        if not proj_name or not client_name:
            return send_json(handler, {"success": False, "error": "Project and client name are required"}, 400)

        proj_id = body.get('id') or f"PRJ-NTW-{uuid.uuid4().hex[:8]}"
        category = body.get('category', 'Decking')
        try:
            total_value = float(body.get('total_value', 0.0))
        except Exception:
            total_value = 0.0
        try:
            sq_ft = float(body.get('sq_ft', 0.0))
        except Exception:
            sq_ft = 0.0
        try:
            discount_pct = float(body.get('discount_pct', 0.0))
        except Exception:
            discount_pct = 0.0
        location = body.get('location', 'Bengaluru, Karnataka')
        city = body.get('city', 'Bengaluru')
        state = body.get('state', 'Karnataka')
        country = body.get('country', 'India')
        financial_year = body.get('financial_year') or _default_fy()
        now = datetime.now()
        month = int(body.get('month') or now.month)

        if body.get('day_bracket'):
            day_bracket = body['day_bracket']
        else:
            d = now.day
            if d <= 5: day_bracket = '1-5'
            elif d <= 10: day_bracket = '6-10'
            elif d <= 15: day_bracket = '11-15'
            elif d <= 20: day_bracket = '16-20'
            elif d <= 25: day_bracket = '21-25'
            else: day_bracket = '26-31'

        stage = body.get('stage', 'Pipeline')
        days_to_win = int(body.get('days_pipeline_to_win') or (1 if stage == 'Win' else 0))
        feedback_pending = 1 if body.get('feedback_pending') in (1, '1', True, 'true', 'True') else 0
        feedback_notes = body.get('feedback_notes', '')
        owner_name = body.get('owner_name') or auth_user.get('full_name', 'Rohan Verma')

        database.execute_commit("""
            INSERT INTO pipeline_projects (id, project_name, client_name, location, city, state, country,
                                          financial_year, month, day_bracket, category, total_value, sq_ft,
                                          discount_pct, days_pipeline_to_win, stage, feedback_pending,
                                          feedback_notes, owner_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (proj_id, proj_name, client_name, location, city, state, country,
              financial_year, month, day_bracket, category, total_value, sq_ft,
              discount_pct, days_to_win, stage, feedback_pending, feedback_notes, owner_name))

        created = database.execute_one("SELECT * FROM pipeline_projects WHERE id = ?;", (proj_id,))
        return send_json(handler, {"success": True, "message": "Project created successfully", "project": dict(created)}, 201)

    # ── Protected: Update Pipeline Project (POST fallback) ───────────────────
    if path == '/api/projects/update':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        return _update_project_internal(handler, body)

    # ── Protected: Delete Pipeline Project (POST fallback) ───────────────────
    if path == '/api/projects/delete':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        proj_id = body.get('id')
        return _delete_project_internal(handler, proj_id)

    # ── Protected: Feedback Pending Workflow (Resolve / Update) ──────────────
    if path == '/api/projects/feedback':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        proj_id = body.get('project_id') or body.get('id')
        if not proj_id:
            return send_json(handler, {"success": False, "error": "project_id is required"}, 400)
        existing = database.execute_one("SELECT * FROM pipeline_projects WHERE id = ?;", (proj_id,))
        if not existing:
            return send_json(handler, {"success": False, "error": "Project not found"}, 404)

        action = (body.get('action') or 'update').lower()
        notes = (body.get('feedback_notes') or body.get('notes') or '').strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        if action == 'resolve':
            feedback_pending = 0
            existing_notes = (existing.get('feedback_notes') or '').strip()
            if notes:
                new_notes = f"{existing_notes} | [Resolved {timestamp}]: {notes}".strip(' |')
            else:
                new_notes = f"{existing_notes} | [Resolved {timestamp}]".strip(' |')
        else:
            feedback_pending = 1
            new_notes = notes or existing.get('feedback_notes') or ''

        database.execute_commit("""
            UPDATE pipeline_projects
            SET feedback_pending = ?, feedback_notes = ?
            WHERE id = ?;
        """, (feedback_pending, new_notes, proj_id))

        updated = database.execute_one("SELECT * FROM pipeline_projects WHERE id = ?;", (proj_id,))
        pending_count = database.execute_one("SELECT COUNT(*) as count FROM pipeline_projects WHERE feedback_pending = 1;")['count']
        return send_json(handler, {
            "success": True,
            "message": "Feedback resolved" if feedback_pending == 0 else "Feedback updated",
            "feedback_pending_count": pending_count,
            "project": dict(updated)
        })

    # ── Protected: Directory Firms CRUD ──────────────────────────────────────
    if path == '/api/directory/firms':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        firm_name = body.get('firm_name', '').strip()
        if not firm_name:
            return send_json(handler, {"success": False, "error": "Firm name is required"}, 400)
        category = body.get('category', 'Architect')
        if category not in ('PRO', 'Architect', 'PROPLUS'):
            category = 'Architect'
        city = body.get('city', 'Bengaluru')
        state = body.get('state', 'Karnataka')
        country = body.get('country', 'India')
        status = body.get('status', 'active')
        firm_id = body.get('id') or f"FRM-NTW-{uuid.uuid4().hex[:8]}"

        database.execute_commit("""
            INSERT INTO directory_firms (id, firm_name, category, city, state, country, status)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (firm_id, firm_name, category, city, state, country, status))

        contacts = body.get('contacts') or []
        for c in contacts:
            first_name = c.get('first_name', '').strip()
            if not first_name:
                continue
            cnt_id = f"CNT-NTW-{uuid.uuid4().hex[:8]}"
            last_name = c.get('last_name', '').strip()
            user_type = c.get('user_type', 'Principal Architect')
            mobile = c.get('mobile', '')
            email = c.get('email', '')
            is_primary = 1 if c.get('is_primary') else 0
            database.execute_commit("""
                INSERT INTO directory_contacts (id, firm_id, first_name, last_name, user_type, mobile, email, is_primary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (cnt_id, firm_id, first_name, last_name, user_type, mobile, email, is_primary))

        created = database.execute_one("SELECT * FROM directory_firms WHERE id = ?;", (firm_id,))
        created_contacts = database.execute_query("SELECT * FROM directory_contacts WHERE firm_id = ?;", (firm_id,))
        res = dict(created)
        res['contacts'] = [dict(c) for c in created_contacts]
        return send_json(handler, {"success": True, "message": "Firm created successfully", "firm": res}, 201)

    if path == '/api/directory/firms/update':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        return _update_firm_internal(handler, body)

    if path == '/api/directory/firms/delete':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        firm_id = body.get('id')
        return _delete_firm_internal(handler, firm_id)

    if path == '/api/directory/contacts':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        firm_id = body.get('firm_id')
        first_name = body.get('first_name', '').strip()
        if not firm_id or not first_name:
            return send_json(handler, {"success": False, "error": "firm_id and first_name are required"}, 400)
        cnt_id = f"CNT-NTW-{uuid.uuid4().hex[:8]}"
        last_name = body.get('last_name', '').strip()
        user_type = body.get('user_type', 'Associate')
        mobile = body.get('mobile', '')
        email = body.get('email', '')
        is_primary = 1 if body.get('is_primary') else 0
        database.execute_commit("""
            INSERT INTO directory_contacts (id, firm_id, first_name, last_name, user_type, mobile, email, is_primary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (cnt_id, firm_id, first_name, last_name, user_type, mobile, email, is_primary))
        created = database.execute_one("SELECT * FROM directory_contacts WHERE id = ?;", (cnt_id,))
        return send_json(handler, {"success": True, "message": "Contact added", "contact": dict(created)}, 201)

    if path == '/api/directory/contacts/delete':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        cnt_id = body.get('id')
        if not cnt_id:
            return send_json(handler, {"success": False, "error": "Contact ID required"}, 400)
        database.execute_commit("DELETE FROM directory_contacts WHERE id = ?;", (cnt_id,))
        return send_json(handler, {"success": True, "message": "Contact deleted"})

    # ── Protected: Directory Meetings Update & Delete ────────────────────────
    if path == '/api/directory/meetings/update':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        return _update_meeting_internal(handler, body)

    if path == '/api/directory/meetings/delete':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        mtg_id = body.get('id')
        return _delete_meeting_internal(handler, mtg_id)

    # ── Protected: Directory Invitations Update, Resend & Delete ─────────────
    if path == '/api/directory/invitations/update':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        return _update_invitation_internal(handler, body)

    if path == '/api/directory/invitations/resend':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        inv_id = body.get('id')
        return _resend_invitation_internal(handler, inv_id)

    if path == '/api/directory/invitations/delete':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        inv_id = body.get('id')
        return _delete_invitation_internal(handler, inv_id)

    # ── Protected: Directory Visitors CRUD ───────────────────────────────────
    if path == '/api/directory/visitors':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        name = body.get('name', '').strip()
        firm = body.get('firm', '').strip()
        if not name or not firm:
            return send_json(handler, {"success": False, "error": "Visitor name and firm are required"}, 400)
        vis_id = body.get('id') or f"VIS-NTW-{uuid.uuid4().hex[:8]}"
        visitor_type = body.get('visitor_type', 'Architect')
        mobile = body.get('mobile', '')
        email = body.get('email', '')
        link_created = body.get('link_created_date') or datetime.now().strftime("%Y-%m-%d")
        form_submitted = body.get('form_submitted_date')
        country = body.get('country', 'India')
        state = body.get('state', 'Karnataka')
        city = body.get('city', 'Bengaluru')
        event_year = body.get('event_year', str(datetime.now().year))

        database.execute_commit("""
            INSERT INTO id_visitors (id, visitor_type, name, mobile, email, firm, link_created_date,
                                     form_submitted_date, country, state, city, event_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (vis_id, visitor_type, name, mobile, email, firm, link_created, form_submitted, country, state, city, event_year))

        created = database.execute_one("SELECT * FROM id_visitors WHERE id = ?;", (vis_id,))
        return send_json(handler, {"success": True, "message": "Visitor created", "visitor": dict(created)}, 201)

    if path == '/api/directory/visitors/update':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        return _update_visitor_internal(handler, body)

    if path == '/api/directory/visitors/delete':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        vis_id = body.get('id')
        return _delete_visitor_internal(handler, vis_id)

    # ── Protected: GoPro Assets CRUD & View Tracker ──────────────────────────
    if path == '/api/gopro/assets':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        subject = body.get('subject', '').strip()
        creator = body.get('creator', '').strip()
        video_url = body.get('video_url', '').strip()
        if not subject or not creator or not video_url:
            return send_json(handler, {"success": False, "error": "Subject, creator and video_url required"}, 400)
        asset_id = body.get('id') or f"GP-NTW-{uuid.uuid4().hex[:8]}"
        file_type = body.get('file_type', 'MP4 Video')
        duration = body.get('duration', '10:00')
        thumbnail_url = body.get('thumbnail_url', '')
        category = body.get('category', 'Installation Guide')

        database.execute_commit("""
            INSERT INTO go_pro_assets (id, subject, creator, file_type, duration, video_url, thumbnail_url, category, views_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0);
        """, (asset_id, subject, creator, file_type, duration, video_url, thumbnail_url, category))

        created = database.execute_one("SELECT * FROM go_pro_assets WHERE id = ?;", (asset_id,))
        return send_json(handler, {"success": True, "message": "GoPro asset created", "asset": dict(created)}, 201)

    if path == '/api/gopro/assets/update':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        return _update_gopro_internal(handler, body)

    if path == '/api/gopro/assets/delete':
        auth_user = require_auth(handler)
        if not auth_user:
            return
        asset_id = body.get('id')
        return _delete_gopro_internal(handler, asset_id)

    if path == '/api/gopro/assets/view':
        asset_id = body.get('id') or body.get('asset_id')
        if not asset_id:
            return send_json(handler, {"success": False, "error": "Asset ID is required"}, 400)
        database.execute_commit("UPDATE go_pro_assets SET views_count = coalesce(views_count, 0) + 1 WHERE id = ?;", (asset_id,))
        updated = database.execute_one("SELECT id, views_count FROM go_pro_assets WHERE id = ?;", (asset_id,))
        return send_json(handler, {"success": True, "views_count": updated['views_count'] if updated else 1})

    send_json(handler, {"error": "Endpoint not found", "path": path}, 404)


# ─── PUT Handler ──────────────────────────────────────────────────────────────
def handle_put(handler):
    try:
        _handle_put_internal(handler)
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        send_json(handler, {"error": "Internal Server Error", "details": str(e)}, 500)

def _handle_put_internal(handler):
    parsed = urlparse(handler.path)
    path = parsed.path.rstrip('/')

    content_length = int(handler.headers.get('Content-Length', 0))
    body_bytes = handler.rfile.read(content_length) if content_length > 0 else b'{}'
    try:
        body = json.loads(body_bytes.decode('utf-8'))
    except Exception:
        body = {}

    if path == '/api/orders' or path.startswith('/api/orders/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        if path.startswith('/api/orders/') and path != '/api/orders':
            body['id'] = path.split('/')[-1]
        return _update_order_internal(handler, body)

    if path == '/api/projects' or path.startswith('/api/projects/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        if path.startswith('/api/projects/') and path != '/api/projects':
            body['id'] = path.split('/')[-1]
        return _update_project_internal(handler, body)

    if path == '/api/directory/firms' or path.startswith('/api/directory/firms/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        if path.startswith('/api/directory/firms/') and path != '/api/directory/firms':
            body['id'] = path.split('/')[-1]
        return _update_firm_internal(handler, body)

    if path == '/api/directory/meetings' or path.startswith('/api/directory/meetings/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        if path.startswith('/api/directory/meetings/') and path != '/api/directory/meetings':
            body['id'] = path.split('/')[-1]
        return _update_meeting_internal(handler, body)

    if path == '/api/directory/invitations' or path.startswith('/api/directory/invitations/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        if path.startswith('/api/directory/invitations/') and path != '/api/directory/invitations':
            body['id'] = path.split('/')[-1]
        return _update_invitation_internal(handler, body)

    if path == '/api/directory/visitors' or path.startswith('/api/directory/visitors/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        if path.startswith('/api/directory/visitors/') and path != '/api/directory/visitors':
            body['id'] = path.split('/')[-1]
        return _update_visitor_internal(handler, body)

    if path == '/api/gopro/assets' or path.startswith('/api/gopro/assets/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        if path.startswith('/api/gopro/assets/') and path != '/api/gopro/assets':
            body['id'] = path.split('/')[-1]
        return _update_gopro_internal(handler, body)

    send_json(handler, {"error": "Endpoint not found", "path": path}, 404)


# ─── DELETE Handler ───────────────────────────────────────────────────────────
def handle_delete(handler):
    try:
        _handle_delete_internal(handler)
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        send_json(handler, {"error": "Internal Server Error", "details": str(e)}, 500)

def _handle_delete_internal(handler):
    parsed = urlparse(handler.path)
    path = parsed.path.rstrip('/')

    content_length = int(handler.headers.get('Content-Length', 0))
    body_bytes = handler.rfile.read(content_length) if content_length > 0 else b'{}'
    try:
        body = json.loads(body_bytes.decode('utf-8'))
    except Exception:
        body = {}

    if path.startswith('/api/vendors/') and path != '/api/vendors/':
        auth_user = require_auth(handler, roles=['admin', 'superadmin'])
        if not auth_user:
            return
        user_id = path.split('/')[-1]
        curr = database.execute_one("SELECT id, role FROM users WHERE id = ? OR vendor_id = ?;", (user_id, user_id))
        if not curr:
            return send_json(handler, {"success": False, "error": "Vendor not found"}, 404)
        if curr['id'] == 'admin' or curr['role'] == 'superadmin':
            return send_json(handler, {"success": False, "error": "Cannot delete root Super Administrator"}, 403)
        database.execute_commit("DELETE FROM sessions WHERE user_id = ?;", (curr['id'],))
        database.execute_commit("DELETE FROM users WHERE id = ?;", (curr['id'],))
        return send_json(handler, {"success": True, "message": "Vendor deleted successfully", "id": curr['id']})

    if path == '/api/vendors':
        auth_user = require_auth(handler, roles=['admin', 'superadmin'])
        if not auth_user:
            return
        user_id = body.get('id') or body.get('vendor_id')
        if not user_id:
            return send_json(handler, {"success": False, "error": "Vendor ID required"}, 400)
        curr = database.execute_one("SELECT id, role FROM users WHERE id = ? OR vendor_id = ?;", (user_id, user_id))
        if not curr:
            return send_json(handler, {"success": False, "error": "Vendor not found"}, 404)
        if curr['id'] == 'admin' or curr['role'] == 'superadmin':
            return send_json(handler, {"success": False, "error": "Cannot delete root Super Administrator"}, 403)
        database.execute_commit("DELETE FROM sessions WHERE user_id = ?;", (curr['id'],))
        database.execute_commit("DELETE FROM users WHERE id = ?;", (curr['id'],))
        return send_json(handler, {"success": True, "message": "Vendor deleted successfully", "id": curr['id']})

    if path == '/api/orders' or path.startswith('/api/orders/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        order_id = path.split('/')[-1] if (path.startswith('/api/orders/') and path != '/api/orders') else body.get('id')
        if not order_id:
            return send_json(handler, {"success": False, "error": "Order ID required"}, 400)
        database.execute_commit("DELETE FROM waltz_orders WHERE id = ?;", (order_id,))
        return send_json(handler, {"success": True, "message": "Order deleted successfully", "id": order_id})

    if path == '/api/projects' or path.startswith('/api/projects/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        proj_id = path.split('/')[-1] if (path.startswith('/api/projects/') and path != '/api/projects') else body.get('id')
        return _delete_project_internal(handler, proj_id)

    if path == '/api/directory/firms' or path.startswith('/api/directory/firms/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        firm_id = path.split('/')[-1] if (path.startswith('/api/directory/firms/') and path != '/api/directory/firms') else body.get('id')
        return _delete_firm_internal(handler, firm_id)

    if path == '/api/directory/contacts' or path.startswith('/api/directory/contacts/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        cnt_id = path.split('/')[-1] if (path.startswith('/api/directory/contacts/') and path != '/api/directory/contacts') else body.get('id')
        if not cnt_id:
            return send_json(handler, {"success": False, "error": "Contact ID required"}, 400)
        database.execute_commit("DELETE FROM directory_contacts WHERE id = ?;", (cnt_id,))
        return send_json(handler, {"success": True, "message": "Contact deleted", "id": cnt_id})

    if path == '/api/directory/meetings' or path.startswith('/api/directory/meetings/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        mtg_id = path.split('/')[-1] if (path.startswith('/api/directory/meetings/') and path != '/api/directory/meetings') else body.get('id')
        return _delete_meeting_internal(handler, mtg_id)

    if path == '/api/directory/invitations' or path.startswith('/api/directory/invitations/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        inv_id = path.split('/')[-1] if (path.startswith('/api/directory/invitations/') and path != '/api/directory/invitations') else body.get('id')
        return _delete_invitation_internal(handler, inv_id)

    if path == '/api/directory/visitors' or path.startswith('/api/directory/visitors/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        vis_id = path.split('/')[-1] if (path.startswith('/api/directory/visitors/') and path != '/api/directory/visitors') else body.get('id')
        return _delete_visitor_internal(handler, vis_id)

    if path == '/api/gopro/assets' or path.startswith('/api/gopro/assets/'):
        auth_user = require_auth(handler)
        if not auth_user:
            return
        asset_id = path.split('/')[-1] if (path.startswith('/api/gopro/assets/') and path != '/api/gopro/assets') else body.get('id')
        return _delete_gopro_internal(handler, asset_id)

    send_json(handler, {"error": "Endpoint not found", "path": path}, 404)


# ─── Order Update Helper ──────────────────────────────────────────────────────
def _update_order_internal(handler, body):
    order_id = body.get('id')
    if not order_id:
        return send_json(handler, {"success": False, "error": "Order ID is required"}, 400)

    existing = database.execute_one("SELECT * FROM waltz_orders WHERE id = ?;", (order_id,))
    if not existing:
        return send_json(handler, {"success": False, "error": "Order not found"}, 404)

    proj_name = body.get('project_name', existing['project_name'])
    client_name = body.get('client_name', existing['client_name'])
    status = body.get('status', existing['status'])
    try:
        final_amount = float(body.get('final_amount', existing['final_amount']))
    except Exception:
        final_amount = existing['final_amount']
    country = body.get('country', existing['country'])
    state = body.get('state', existing['state'])
    city = body.get('city', existing['city'])
    source = body.get('source', existing['source'])
    notes = body.get('notes', existing['notes'])
    owner_name = body.get('owner_name', existing.get('owner_name', 'Rohan Verma'))

    database.execute_commit("""
        UPDATE waltz_orders
        SET project_name = ?, client_name = ?, status = ?, final_amount = ?,
            country = ?, state = ?, city = ?, source = ?, notes = ?, owner_name = ?
        WHERE id = ?;
    """, (proj_name, client_name, status, final_amount, country, state, city, source, notes, owner_name, order_id))

    updated = database.execute_one("SELECT * FROM waltz_orders WHERE id = ?;", (order_id,))
    return send_json(handler, {"success": True, "message": "Order updated", "order": dict(updated)})


# ─── Project Update Helper (With Auto Pipeline → Win Days Calculation) ──────
def _update_project_internal(handler, body):
    proj_id = body.get('id')
    if not proj_id:
        return send_json(handler, {"success": False, "error": "Project ID is required"}, 400)
    existing = database.execute_one("SELECT * FROM pipeline_projects WHERE id = ?;", (proj_id,))
    if not existing:
        return send_json(handler, {"success": False, "error": "Project not found"}, 404)

    proj_name = body.get('project_name', existing['project_name'])
    client_name = body.get('client_name', existing['client_name'])
    category = body.get('category', existing['category'])
    try:
        total_value = float(body.get('total_value', existing['total_value']))
    except Exception:
        total_value = existing['total_value']
    try:
        sq_ft = float(body.get('sq_ft', existing['sq_ft']))
    except Exception:
        sq_ft = existing['sq_ft']
    try:
        discount_pct = float(body.get('discount_pct', existing['discount_pct']))
    except Exception:
        discount_pct = existing['discount_pct']
    location = body.get('location', existing['location'])
    city = body.get('city', existing['city'])
    state = body.get('state', existing['state'])
    country = body.get('country', existing.get('country', 'India'))
    financial_year = body.get('financial_year', existing['financial_year'])
    try:
        month = int(body.get('month', existing['month']))
    except Exception:
        month = existing['month']
    day_bracket = body.get('day_bracket', existing['day_bracket'])
    stage = body.get('stage', existing['stage'])

    # Auto-calculate days_pipeline_to_win on Pipeline -> Win transition
    days_to_win = existing.get('days_pipeline_to_win') or 0
    if stage == 'Win' and existing.get('stage') != 'Win':
        if 'days_pipeline_to_win' in body and body['days_pipeline_to_win'] is not None:
            try:
                days_to_win = int(body['days_pipeline_to_win'])
            except Exception:
                days_to_win = 1
        else:
            created_at_str = str(existing.get('created_at') or '')
            try:
                if 'T' in created_at_str:
                    c_dt = datetime.fromisoformat(created_at_str.replace('Z', ''))
                elif ' ' in created_at_str:
                    c_dt = datetime.strptime(created_at_str[:19], '%Y-%m-%d %H:%M:%S')
                else:
                    c_dt = datetime.strptime(created_at_str[:10], '%Y-%m-%d')
                diff_days = (datetime.now() - c_dt).days
                days_to_win = max(1, diff_days)
            except Exception:
                days_to_win = 1
    elif 'days_pipeline_to_win' in body and body['days_pipeline_to_win'] is not None:
        try:
            days_to_win = int(body['days_pipeline_to_win'])
        except Exception:
            days_to_win = existing.get('days_pipeline_to_win') or 0

    if 'feedback_pending' in body:
        feedback_pending = 1 if body['feedback_pending'] in (1, '1', True, 'true', 'True') else 0
    else:
        feedback_pending = existing.get('feedback_pending', 0)

    feedback_notes = body.get('feedback_notes', existing.get('feedback_notes', ''))
    owner_name = body.get('owner_name', existing.get('owner_name', 'Rohan Verma'))

    database.execute_commit("""
        UPDATE pipeline_projects
        SET project_name = ?, client_name = ?, category = ?, total_value = ?, sq_ft = ?,
            discount_pct = ?, location = ?, city = ?, state = ?, country = ?,
            financial_year = ?, month = ?, day_bracket = ?, stage = ?,
            days_pipeline_to_win = ?, feedback_pending = ?, feedback_notes = ?, owner_name = ?
        WHERE id = ?;
    """, (proj_name, client_name, category, total_value, sq_ft, discount_pct,
          location, city, state, country, financial_year, month, day_bracket,
          stage, days_to_win, feedback_pending, feedback_notes, owner_name, proj_id))

    updated = database.execute_one("SELECT * FROM pipeline_projects WHERE id = ?;", (proj_id,))
    return send_json(handler, {"success": True, "message": "Project updated successfully", "project": dict(updated)})

def _delete_project_internal(handler, proj_id):
    if not proj_id:
        return send_json(handler, {"success": False, "error": "Project ID is required"}, 400)
    database.execute_commit("DELETE FROM pipeline_projects WHERE id = ?;", (proj_id,))
    return send_json(handler, {"success": True, "message": "Project deleted successfully", "id": proj_id})


# ─── Directory Firm Helpers ──────────────────────────────────────────────────
def _update_firm_internal(handler, body):
    firm_id = body.get('id')
    if not firm_id:
        return send_json(handler, {"success": False, "error": "Firm ID is required"}, 400)
    existing = database.execute_one("SELECT * FROM directory_firms WHERE id = ?;", (firm_id,))
    if not existing:
        return send_json(handler, {"success": False, "error": "Firm not found"}, 404)

    firm_name = body.get('firm_name', existing['firm_name']).strip()
    category = body.get('category', existing['category'])
    if category not in ('PRO', 'Architect', 'PROPLUS'):
        category = existing['category']
    city = body.get('city', existing['city'])
    state = body.get('state', existing['state'])
    country = body.get('country', existing.get('country', 'India'))
    status = body.get('status', existing.get('status', 'active'))

    database.execute_commit("""
        UPDATE directory_firms
        SET firm_name = ?, category = ?, city = ?, state = ?, country = ?, status = ?
        WHERE id = ?;
    """, (firm_name, category, city, state, country, status, firm_id))

    updated = database.execute_one("SELECT * FROM directory_firms WHERE id = ?;", (firm_id,))
    contacts = database.execute_query("SELECT * FROM directory_contacts WHERE firm_id = ?;", (firm_id,))
    res = dict(updated)
    res['contacts'] = [dict(c) for c in contacts]
    return send_json(handler, {"success": True, "message": "Firm updated successfully", "firm": res})

def _delete_firm_internal(handler, firm_id):
    if not firm_id:
        return send_json(handler, {"success": False, "error": "Firm ID is required"}, 400)
    database.execute_commit("DELETE FROM directory_contacts WHERE firm_id = ?;", (firm_id,))
    database.execute_commit("DELETE FROM directory_firms WHERE id = ?;", (firm_id,))
    return send_json(handler, {"success": True, "message": "Firm and associated contacts deleted successfully", "id": firm_id})


# ─── Directory Meeting Helpers ───────────────────────────────────────────────
def _update_meeting_internal(handler, body):
    mtg_id = body.get('id')
    if not mtg_id:
        return send_json(handler, {"success": False, "error": "Meeting ID is required"}, 400)
    existing = database.execute_one("SELECT * FROM meetings WHERE id = ?;", (mtg_id,))
    if not existing:
        return send_json(handler, {"success": False, "error": "Meeting not found"}, 404)

    meeting_date = body.get('meeting_date', existing['meeting_date'])
    firm_name = body.get('firm_name', existing['firm_name'])
    guest_name = body.get('guest_name', existing['guest_name'])
    mobile = body.get('mobile', existing['mobile'])
    user_type = body.get('user_type', existing['user_type'])
    guest_type = body.get('guest_type', existing['guest_type'])
    country = body.get('country', existing.get('country', 'India'))
    state = body.get('state', existing.get('state', 'Karnataka'))
    city = body.get('city', existing.get('city', 'Bengaluru'))
    status = body.get('status', existing.get('status', 'Completed'))
    discussion_notes = body.get('discussion_notes', existing.get('discussion_notes', ''))
    owner_name = body.get('owner_name', existing.get('owner_name', 'Rohan Verma'))

    database.execute_commit("""
        UPDATE meetings
        SET meeting_date = ?, firm_name = ?, guest_name = ?, mobile = ?,
            user_type = ?, guest_type = ?, country = ?, state = ?, city = ?,
            status = ?, discussion_notes = ?, owner_name = ?
        WHERE id = ?;
    """, (meeting_date, firm_name, guest_name, mobile, user_type, guest_type,
          country, state, city, status, discussion_notes, owner_name, mtg_id))

    updated = database.execute_one("SELECT * FROM meetings WHERE id = ?;", (mtg_id,))
    return send_json(handler, {"success": True, "message": "Meeting updated successfully", "meeting": dict(updated)})

def _delete_meeting_internal(handler, mtg_id):
    if not mtg_id:
        return send_json(handler, {"success": False, "error": "Meeting ID is required"}, 400)
    database.execute_commit("DELETE FROM meetings WHERE id = ?;", (mtg_id,))
    return send_json(handler, {"success": True, "message": "Meeting deleted successfully", "id": mtg_id})


# ─── Directory Invitation Helpers ─────────────────────────────────────────────
def _update_invitation_internal(handler, body):
    inv_id = body.get('id')
    if not inv_id:
        return send_json(handler, {"success": False, "error": "Invitation ID is required"}, 400)
    existing = database.execute_one("SELECT * FROM id_invitations WHERE id = ?;", (inv_id,))
    if not existing:
        return send_json(handler, {"success": False, "error": "Invitation not found"}, 404)

    status = body.get('status', existing.get('status', 'Active'))
    recipient_name = body.get('recipient_name', existing['recipient_name'])
    firm_name = body.get('firm_name', existing['firm_name'])
    recipient_email = body.get('recipient_email', existing['recipient_email'])
    mobile = body.get('mobile', existing['mobile'])

    database.execute_commit("""
        UPDATE id_invitations
        SET status = ?, recipient_name = ?, firm_name = ?, recipient_email = ?, mobile = ?
        WHERE id = ?;
    """, (status, recipient_name, firm_name, recipient_email, mobile, inv_id))

    updated = database.execute_one("SELECT * FROM id_invitations WHERE id = ?;", (inv_id,))
    return send_json(handler, {"success": True, "message": "Invitation updated successfully", "invitation": dict(updated)})

def _resend_invitation_internal(handler, inv_id):
    if not inv_id:
        return send_json(handler, {"success": False, "error": "Invitation ID is required"}, 400)
    existing = database.execute_one("SELECT * FROM id_invitations WHERE id = ?;", (inv_id,))
    if not existing:
        return send_json(handler, {"success": False, "error": "Invitation not found"}, 404)

    new_expiry = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    database.execute_commit("""
        UPDATE id_invitations
        SET status = 'Active', expires_at = ?
        WHERE id = ?;
    """, (new_expiry, inv_id))

    updated = database.execute_one("SELECT * FROM id_invitations WHERE id = ?;", (inv_id,))
    return send_json(handler, {"success": True, "message": "Invitation validity extended by 30 days", "invitation": dict(updated)})

def _delete_invitation_internal(handler, inv_id):
    if not inv_id:
        return send_json(handler, {"success": False, "error": "Invitation ID is required"}, 400)
    database.execute_commit("DELETE FROM id_invitations WHERE id = ?;", (inv_id,))
    return send_json(handler, {"success": True, "message": "Invitation deleted successfully", "id": inv_id})


# ─── Directory Visitor Helpers ───────────────────────────────────────────────
def _update_visitor_internal(handler, body):
    vis_id = body.get('id')
    if not vis_id:
        return send_json(handler, {"success": False, "error": "Visitor ID is required"}, 400)
    existing = database.execute_one("SELECT * FROM id_visitors WHERE id = ?;", (vis_id,))
    if not existing:
        return send_json(handler, {"success": False, "error": "Visitor not found"}, 404)

    name = body.get('name', existing['name'])
    firm = body.get('firm', existing['firm'])
    visitor_type = body.get('visitor_type', existing['visitor_type'])
    mobile = body.get('mobile', existing['mobile'])
    email = body.get('email', existing['email'])
    country = body.get('country', existing.get('country', 'India'))
    state = body.get('state', existing.get('state', 'Karnataka'))
    city = body.get('city', existing.get('city', 'Bengaluru'))
    event_year = body.get('event_year', existing.get('event_year', str(datetime.now().year)))
    form_submitted_date = body.get('form_submitted_date', existing.get('form_submitted_date'))

    database.execute_commit("""
        UPDATE id_visitors
        SET name = ?, firm = ?, visitor_type = ?, mobile = ?, email = ?,
            country = ?, state = ?, city = ?, event_year = ?, form_submitted_date = ?
        WHERE id = ?;
    """, (name, firm, visitor_type, mobile, email, country, state, city, event_year, form_submitted_date, vis_id))

    updated = database.execute_one("SELECT * FROM id_visitors WHERE id = ?;", (vis_id,))
    return send_json(handler, {"success": True, "message": "Visitor updated successfully", "visitor": dict(updated)})

def _delete_visitor_internal(handler, vis_id):
    if not vis_id:
        return send_json(handler, {"success": False, "error": "Visitor ID is required"}, 400)
    database.execute_commit("DELETE FROM id_visitors WHERE id = ?;", (vis_id,))
    return send_json(handler, {"success": True, "message": "Visitor deleted successfully", "id": vis_id})


# ─── GoPro Asset Helpers ─────────────────────────────────────────────────────
def _update_gopro_internal(handler, body):
    asset_id = body.get('id')
    if not asset_id:
        return send_json(handler, {"success": False, "error": "Asset ID is required"}, 400)
    existing = database.execute_one("SELECT * FROM go_pro_assets WHERE id = ?;", (asset_id,))
    if not existing:
        return send_json(handler, {"success": False, "error": "GoPro asset not found"}, 404)

    subject = body.get('subject', existing['subject'])
    creator = body.get('creator', existing['creator'])
    file_type = body.get('file_type', existing.get('file_type', 'MP4 Video'))
    duration = body.get('duration', existing['duration'])
    video_url = body.get('video_url', existing['video_url'])
    thumbnail_url = body.get('thumbnail_url', existing.get('thumbnail_url'))
    category = body.get('category', existing.get('category', 'Installation Guide'))

    database.execute_commit("""
        UPDATE go_pro_assets
        SET subject = ?, creator = ?, file_type = ?, duration = ?,
            video_url = ?, thumbnail_url = ?, category = ?
        WHERE id = ?;
    """, (subject, creator, file_type, duration, video_url, thumbnail_url, category, asset_id))

    updated = database.execute_one("SELECT * FROM go_pro_assets WHERE id = ?;", (asset_id,))
    return send_json(handler, {"success": True, "message": "GoPro asset updated successfully", "asset": dict(updated)})

def _delete_gopro_internal(handler, asset_id):
    if not asset_id:
        return send_json(handler, {"success": False, "error": "Asset ID is required"}, 400)
    database.execute_commit("DELETE FROM go_pro_assets WHERE id = ?;", (asset_id,))
    return send_json(handler, {"success": True, "message": "GoPro asset deleted successfully", "id": asset_id})

