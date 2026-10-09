"""REST API Router for NewTechWood CRM SQLite backend."""
import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

# Ensure db directory is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

import database

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

def get_auth_user(handler):
    auth_header = handler.headers.get('Authorization', '')
    token = None
    if auth_header.startswith('Bearer '):
        token = auth_header[7:].strip()
    
    if not token:
        # Check query params for token
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
        "SELECT id, email, full_name, role, status, avatar_initials, created_at FROM users WHERE id = ?;",
        (session['user_id'],)
    )
    return user

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

    # Health check
    if path == '/api/health':
        user_count = database.execute_one("SELECT COUNT(*) as count FROM users;")['count']
        project_count = database.execute_one("SELECT COUNT(*) as count FROM pipeline_projects;")['count']
        order_count = database.execute_one("SELECT COUNT(*) as count FROM waltz_orders;")['count']
        return send_json(handler, {
            "status": "ok",
            "database": "connected",
            "timestamp": datetime.now().isoformat(),
            "counts": {
                "users": user_count,
                "projects": project_count,
                "orders": order_count
            }
        })

    # Get Current Session User
    if path == '/api/auth/me':
        user = get_auth_user(handler)
        if not user:
            return send_json(handler, {"success": False, "error": "Unauthorized or session expired"}, 401)
        return send_json(handler, {"success": True, "user": user})

    # List Users (Admin Only)
    if path == '/api/users':
        users = database.execute_query("SELECT id, email, full_name, role, status, avatar_initials, created_at FROM users;")
        return send_json(handler, {"success": True, "users": users})

    # CRM Dashboard Aggregates, Charts, & KPIs
    if path == '/api/dashboard':
        fy = qs.get('financial_year', ['FY 25-26'])[0].strip()
        months_param = qs.get('months', [''])[0].strip()
        chart_type = qs.get('chart_type', ['revenue'])[0].strip()

        # Parse months list if provided (e.g. "4,5,6,7,8,9,10,11,12,1,2,3")
        selected_months = []
        if months_param:
            try:
                selected_months = [int(m.strip()) for m in months_param.split(',') if m.strip()]
            except Exception:
                selected_months = []

        # Build SQL condition
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

        # Fetch projects matching filters
        projects = database.execute_query(f"""
            SELECT id, project_name, client_name, location, city, state, country,
                   financial_year, month, day_bracket, category, total_value, sq_ft,
                   discount_pct, days_pipeline_to_win, stage, feedback_pending, feedback_notes,
                   coalesce(owner_name, 'Rohan Verma') as owner_name
            FROM pipeline_projects
            {where_sql}
            ORDER BY total_value DESC;
        """, tuple(params))

        # 1. Feedback Pending Alert Banner
        feedback_pending_projects = [dict(p) for p in projects if p.get('feedback_pending') == 1]
        feedback_pending_count = len(feedback_pending_projects)

        # 2. Pipeline KPIs
        pipeline_projects = [dict(p) for p in projects if p.get('stage') == 'Pipeline']
        pipeline_total_val = sum(float(p.get('total_value', 0)) for p in pipeline_projects)
        pipeline_count = len(pipeline_projects)
        pipeline_avg_discount = round(sum(float(p.get('discount_pct', 0)) for p in pipeline_projects) / pipeline_count, 1) if pipeline_count > 0 else 0.0

        # 3. Win KPIs
        win_projects = [dict(p) for p in projects if p.get('stage') == 'Win']
        win_total_val = sum(float(p.get('total_value', 0)) for p in win_projects)
        win_count = len(win_projects)
        win_avg_days = round(sum(int(p.get('days_pipeline_to_win', 0)) for p in win_projects) / win_count, 1) if win_count > 0 else 0.0
        win_avg_discount = round(sum(float(p.get('discount_pct', 0)) for p in win_projects) / win_count, 1) if win_count > 0 else 0.0

        # 4. Line Chart: Total Projects (Win vs Pipeline by Day Bracket)
        brackets = ['1-5', '6-10', '11-15', '16-20', '21-25', '26-31']
        line_chart_win = []
        line_chart_pipe = []
        for b in brackets:
            w_c = sum(1 for p in win_projects if p.get('day_bracket') == b)
            p_c = sum(1 for p in pipeline_projects if p.get('day_bracket') == b)
            line_chart_win.append(w_c)
            line_chart_pipe.append(p_c)

        # 5. Monthly Bar Chart: Apr-Mar Pipeline vs Win (in INR Cr)
        fy_months = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]
        fy_month_labels = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
        bar_chart_pipeline_cr = []
        bar_chart_win_cr = []
        for m in fy_months:
            p_sum = sum(float(p.get('total_value', 0)) for p in pipeline_projects if p.get('month') == m)
            w_sum = sum(float(p.get('total_value', 0)) for p in win_projects if p.get('month') == m)
            bar_chart_pipeline_cr.append(round(p_sum / 10000000.0, 2))
            bar_chart_win_cr.append(round(w_sum / 10000000.0, 2))

        # 6. Product Breakdown (Amount & Sq.Ft)
        categories = sorted(list(set(p.get('category', 'Other') for p in projects if p.get('category'))))
        product_breakdown = []
        for cat in categories:
            cat_projects = [p for p in projects if p.get('category') == cat]
            c_amount = sum(float(p.get('total_value', 0)) for p in cat_projects)
            c_sqft = sum(float(p.get('sq_ft', 0)) for p in cat_projects)
            product_breakdown.append({
                "category": cat,
                "amount": c_amount,
                "amount_cr": round(c_amount / 10000000.0, 2),
                "sq_ft": c_sqft,
                "count": len(cat_projects)
            })

        # 7. Traffic Light Dashboard Items
        traffic_light_items = []
        for p in projects:
            p_dict = dict(p)
            disc = float(p_dict.get('discount_pct', 0))
            is_fb = bool(p_dict.get('feedback_pending', 0))
            stg = p_dict.get('stage')

            if is_fb:
                light = 'red'
                reason = f'Feedback Pending ({p_dict.get("feedback_notes") or "Awaiting client response"})'
            elif disc > 12.0 and stg == 'Pipeline':
                light = 'amber'
                reason = f'High Discount Requested ({disc}%)'
            elif stg == 'Pipeline':
                light = 'amber'
                reason = 'Active Negotiation / BOQ Review'
            elif stg == 'Win':
                light = 'green'
                reason = f'Won & Invoiced ({p_dict.get("days_pipeline_to_win", 0)} days)'
            else:
                light = 'red'
                reason = 'Lost Deal'

            p_dict['traffic_light'] = light
            p_dict['traffic_reason'] = reason
            traffic_light_items.append(p_dict)

        # 8. Top 10 Pipeline Projects
        top_10_pipeline = pipeline_projects[:10]

        # Available Financial Years in DB
        all_fys = database.execute_query("SELECT DISTINCT financial_year FROM pipeline_projects ORDER BY financial_year DESC;")
        distinct_fys = [row['financial_year'] for row in all_fys if row.get('financial_year')]

        return send_json(handler, {
            "success": True,
            "filters": {
                "financial_year": fy,
                "months": selected_months,
                "chart_type": chart_type
            },
            "available_fys": distinct_fys,
            "alert": {
                "feedback_pending_count": feedback_pending_count,
                "feedback_pending_projects": feedback_pending_projects
            },
            "kpis": {
                "pipeline": {
                    "total_value": pipeline_total_val,
                    "count": pipeline_count,
                    "avg_discount": pipeline_avg_discount
                },
                "win": {
                    "total_value": win_total_val,
                    "count": win_count,
                    "avg_days": win_avg_days,
                    "avg_discount": win_avg_discount
                }
            },
            "charts": {
                "line_chart": {
                    "labels": brackets,
                    "win_series": line_chart_win,
                    "pipeline_series": line_chart_pipe
                },
                "bar_chart": {
                    "months": fy_month_labels,
                    "month_nums": fy_months,
                    "pipeline_cr": bar_chart_pipeline_cr,
                    "win_cr": bar_chart_win_cr
                },
                "product_breakdown": product_breakdown
            },
            "traffic_light": traffic_light_items,
            "top_10_pipeline": top_10_pipeline,
            "all_projects_count": len(projects)
        })

    # Analytics & Commercial Activity Aggregates
    if path == '/api/analytics':
        from_date = qs.get('from_date', [''])[0].strip()
        to_date = qs.get('to_date', [''])[0].strip()
        user_filter = qs.get('user', ['all'])[0].strip()
        status_filter = qs.get('status', ['all'])[0].strip()

        # 1. Fetch Waltz Orders
        orders = database.execute_query("""
            SELECT id, order_number as ref_no, project_name as title, client_name as client,
                   city, state, order_date as activity_date, status, final_amount as amount,
                   source, coalesce(owner_name, 'Rohan Verma') as owner_name, 'Waltz Order' as activity_type
            FROM waltz_orders;
        """)

        # 2. Fetch Pipeline Projects
        projects = database.execute_query("""
            SELECT id, id as ref_no, project_name as title, client_name as client,
                   city, state, financial_year, month, day_bracket, stage as status,
                   total_value as amount, category as source, coalesce(owner_name, 'Rohan Verma') as owner_name,
                   'Pipeline Project' as activity_type
            FROM pipeline_projects;
        """)

        # 3. Fetch Meetings
        meetings = database.execute_query("""
            SELECT id, id as ref_no, firm_name as title, guest_name as client,
                   city, state, meeting_date as activity_date, 'Completed' as status,
                   0.0 as amount, guest_type as source, coalesce(owner_name, 'Rohan Verma') as owner_name,
                   'Architect Meeting' as activity_type
            FROM meetings;
        """)

        # Normalize project activity dates
        bracket_days = {'1-5': '03', '6-10': '08', '11-15': '13', '16-20': '18', '21-25': '23', '26-31': '28'}
        normalized_projects = []
        for p in projects:
            p_dict = dict(p)
            m = p_dict.get('month', 10)
            year = 2025 if m >= 4 else 2026
            b = p_dict.get('day_bracket', '1-5')
            day = bracket_days.get(b, '15')
            p_dict['activity_date'] = f"{year}-{m:02d}-{day}"
            normalized_projects.append(p_dict)

        # Combine all commercial activities
        all_activities = [dict(o) for o in orders] + normalized_projects + [dict(m) for m in meetings]

        # Distinct owners for filter dropdown
        distinct_users = sorted(list(set(a['owner_name'] for a in all_activities if a.get('owner_name'))))

        # Filter activities
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
                if status_filter.lower() == 'win' and a.get('status') not in ('Win', 'Completed'):
                    continue
                elif status_filter.lower() == 'pipeline' and a.get('status') != 'Pipeline':
                    continue
                elif status_filter.lower() == 'lost' and a.get('status') != 'Lost':
                    continue
            filtered.append(a)

        # Sort chronological descending
        filtered.sort(key=lambda x: x.get('activity_date', ''), reverse=True)

        # Calculate metrics
        total_activities = len(filtered)
        total_revenue = sum(float(x.get('amount', 0)) for x in filtered if x.get('status') in ('Win', 'Completed'))
        total_pipeline = sum(float(x.get('amount', 0)) for x in filtered if x.get('status') == 'Pipeline')
        total_lost = sum(float(x.get('amount', 0)) for x in filtered if x.get('status') == 'Lost')
        won_count = sum(1 for x in filtered if x.get('status') in ('Win', 'Completed') and float(x.get('amount', 0)) > 0)
        pipeline_count = sum(1 for x in filtered if x.get('status') == 'Pipeline')
        lost_count = sum(1 for x in filtered if x.get('status') == 'Lost')
        meetings_count = sum(1 for x in filtered if x.get('activity_type') == 'Architect Meeting')

        closed_total = won_count + lost_count
        win_rate = round((won_count / closed_total * 100), 1) if closed_total > 0 else 0.0
        avg_deal_size = round(total_revenue / won_count, 0) if won_count > 0 else 0.0

        return send_json(handler, {
            "success": True,
            "filters": {
                "from_date": from_date,
                "to_date": to_date,
                "user": user_filter,
                "status": status_filter
            },
            "metrics": {
                "total_activities": total_activities,
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

    # Directory Master: Firms & Contacts
    if path == '/api/directory/firms':
        search = qs.get('search', [''])[0].strip().lower()
        category = qs.get('category', ['all'])[0].strip()

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

    # Meetings
    if path == '/api/directory/meetings':
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
            where_clauses.append("meeting_date >= ?")
            params.append(from_date)
        if to_date:
            where_clauses.append("meeting_date <= ?")
            params.append(to_date)
        if firm_name:
            where_clauses.append("lower(firm_name) LIKE ?")
            params.append(f"%{firm_name}%")
        if guest_name:
            where_clauses.append("lower(guest_name) LIKE ?")
            params.append(f"%{guest_name}%")
        if mobile:
            where_clauses.append("mobile LIKE ?")
            params.append(f"%{mobile}%")
        if user_type and user_type.lower() != 'all':
            where_clauses.append("user_type = ?")
            params.append(user_type)
        if guest_type and guest_type.lower() != 'all':
            where_clauses.append("guest_type = ?")
            params.append(guest_type)
        if country and country.lower() != 'all':
            where_clauses.append("country = ?")
            params.append(country)
        if state and state.lower() != 'all':
            where_clauses.append("state = ?")
            params.append(state)
        if city and city.lower() != 'all':
            where_clauses.append("city = ?")
            params.append(city)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        meetings = database.execute_query(f"""
            SELECT id, meeting_date, firm_name, guest_name, mobile, user_type,
                   guest_type, country, state, city, status, discussion_notes, image_urls
            FROM meetings
            {where_sql}
            ORDER BY meeting_date DESC;
        """, tuple(params))
        return send_json(handler, {"success": True, "count": len(meetings), "meetings": [dict(m) for m in meetings]})

    # ID Invitations
    if path == '/api/directory/invitations':
        invitations = database.execute_query("""
            SELECT id, invitation_code, recipient_name, firm_name, recipient_email,
                   mobile, invitation_link, status, created_at, expires_at
            FROM id_invitations
            ORDER BY created_at DESC;
        """)
        return send_json(handler, {"success": True, "count": len(invitations), "invitations": [dict(i) for i in invitations]})

    # ID Visitors (with 25 rows per page pagination)
    if path == '/api/directory/visitors':
        import math
        try:
            page = int(qs.get('page', ['1'])[0])
        except Exception:
            page = 1
        try:
            limit = int(qs.get('limit', ['25'])[0])
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
            where_clauses.append("visitor_type = ?")
            params.append(visitor_type)
        if name:
            where_clauses.append("lower(name) LIKE ?")
            params.append(f"%{name}%")
        if mobile:
            where_clauses.append("mobile LIKE ?")
            params.append(f"%{mobile}%")
        if email:
            where_clauses.append("lower(email) LIKE ?")
            params.append(f"%{email}%")
        if firm:
            where_clauses.append("lower(firm) LIKE ?")
            params.append(f"%{firm}%")
        if from_created:
            where_clauses.append("link_created_date >= ?")
            params.append(from_created)
        if to_created:
            where_clauses.append("link_created_date <= ?")
            params.append(to_created)
        if country and country.lower() != 'all':
            where_clauses.append("country = ?")
            params.append(country)
        if state and state.lower() != 'all':
            where_clauses.append("state = ?")
            params.append(state)
        if city and city.lower() != 'all':
            where_clauses.append("city = ?")
            params.append(city)
        if event_year and event_year.lower() != 'all':
            where_clauses.append("event_year = ?")
            params.append(event_year)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        total_row = database.execute_one(f"SELECT COUNT(*) as count FROM id_visitors {where_sql};", tuple(params))
        total_count = total_row['count'] if total_row else 0
        total_pages = max(1, math.ceil(total_count / limit))

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
            "success": True,
            "total": total_count,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "visitors": [dict(v) for v in visitors]
        })

    # Go Pro Education Assets
    if path == '/api/gopro/assets':
        subject = qs.get('subject', [''])[0].strip().lower()
        creator = qs.get('creator', [''])[0].strip().lower()
        file_type = qs.get('file_type', [''])[0].strip()

        where_clauses = []
        params = []
        if subject:
            where_clauses.append("lower(subject) LIKE ?")
            params.append(f"%{subject}%")
        if creator:
            where_clauses.append("lower(creator) LIKE ?")
            params.append(f"%{creator}%")
        if file_type and file_type.lower() != 'all':
            where_clauses.append("file_type = ?")
            params.append(file_type)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        assets = database.execute_query(f"""
            SELECT id, subject, creator, file_type, duration, video_url, thumbnail_url, category, views_count
            FROM go_pro_assets
            {where_sql}
            ORDER BY id ASC;
        """, tuple(params))
        return send_json(handler, {"success": True, "count": len(assets), "assets": [dict(a) for a in assets]})

    # Waltz Orders
    if path == '/api/orders':
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
            where_clauses.append("lower(order_number) LIKE ?")
            params.append(f"%{order_number}%")
        if project_name:
            where_clauses.append("lower(project_name) LIKE ?")
            params.append(f"%{project_name}%")
        if client_name:
            where_clauses.append("lower(client_name) LIKE ?")
            params.append(f"%{client_name}%")
        if country and country.lower() != 'all':
            where_clauses.append("country = ?")
            params.append(country)
        if state and state.lower() != 'all':
            where_clauses.append("state = ?")
            params.append(state)
        if city and city.lower() != 'all':
            where_clauses.append("city = ?")
            params.append(city)
        if from_date:
            where_clauses.append("order_date >= ?")
            params.append(from_date)
        if to_date:
            where_clauses.append("order_date <= ?")
            params.append(to_date)
        if status_filter and status_filter.lower() != 'all':
            where_clauses.append("status = ?")
            params.append(status_filter)
        if source and source.lower() != 'all':
            where_clauses.append("source = ?")
            params.append(source)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        orders = database.execute_query(f"""
            SELECT id, order_number, project_name, client_name, country, state, city,
                   order_date, status, final_amount, source, notes, created_at
            FROM waltz_orders
            {where_sql}
            ORDER BY order_date DESC;
        """, tuple(params))
        return send_json(handler, {"success": True, "count": len(orders), "orders": [dict(o) for o in orders]})

    send_json(handler, {"error": "Endpoint not found", "path": path}, 404)

def handle_post(handler):
    parsed = urlparse(handler.path)
    path = parsed.path.rstrip('/')

    content_length = int(handler.headers.get('Content-Length', 0))
    body_bytes = handler.rfile.read(content_length) if content_length > 0 else b'{}'
    try:
        body = json.loads(body_bytes.decode('utf-8'))
    except Exception:
        body = {}

    # Login
    if path == '/api/auth/login':
        email = (body.get('email') or '').strip().lower()
        password = (body.get('password') or '').strip()
        remember = bool(body.get('remember', False))

        if not email or not password:
            return send_json(handler, {"success": False, "error": "Email and password are required"}, 400)

        # Look up user by email or username
        user = database.execute_one(
            "SELECT * FROM users WHERE (lower(email) = ? OR lower(id) = ?) AND status = 'active';",
            (email, email)
        )

        if not user or user['password'] != password:
            return send_json(handler, {"success": False, "error": "Invalid username or password"}, 401)

        # Generate session token
        token = 'ntw_' + uuid.uuid4().hex
        expires_days = 30 if remember else 1
        expires_at = (datetime.now() + timedelta(days=expires_days)).strftime("%Y-%m-%d %H:%M:%S")

        database.execute_commit(
            "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?);",
            (token, user['id'], expires_at)
        )

        safe_user = {
            "id": user['id'],
            "email": user['email'],
            "full_name": user['full_name'],
            "role": user['role'],
            "status": user['status'],
            "avatar_initials": user['avatar_initials'] or user['full_name'][:2].upper()
        }

        return send_json(handler, {
            "success": True,
            "token": token,
            "expires_at": expires_at,
            "user": safe_user
        })

    # Logout
    if path == '/api/auth/logout':
        auth_header = handler.headers.get('Authorization', '')
        token = auth_header[7:].strip() if auth_header.startswith('Bearer ') else body.get('token')
        if token:
            database.execute_commit("DELETE FROM sessions WHERE token = ?;", (token,))
        return send_json(handler, {"success": True, "message": "Logged out successfully"})

    # Create Waltz Order
    if path == '/api/orders':
        proj_name = body.get('project_name', '').strip()
        client_name = body.get('client_name', '').strip()
        order_num = body.get('order_number', '').strip()
        if not order_num:
            order_num = f"WO-2026-{uuid.uuid4().hex[:6].upper()}"
        if not proj_name or not client_name:
            return send_json(handler, {"success": False, "error": "Project and client name are required"}, 400)

        order_id = f"ORD-W-{uuid.uuid4().hex[:8]}"
        country = body.get('country', 'India')
        state = body.get('state', 'Maharashtra')
        city = body.get('city', 'Mumbai')
        order_date = body.get('order_date') or datetime.now().strftime("%Y-%m-%d")
        status = body.get('status', 'Pipeline')
        try:
            final_amount = float(body.get('final_amount', 0.0))
        except Exception:
            final_amount = 0.0
        source = body.get('source', 'Direct Architect')
        notes = body.get('notes', '')

        database.execute_commit("""
            INSERT INTO waltz_orders (id, order_number, project_name, client_name, country, state, city,
                                      order_date, status, final_amount, source, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (order_id, order_num, proj_name, client_name, country, state, city, order_date, status, final_amount, source, notes))

        created = database.execute_one("SELECT * FROM waltz_orders WHERE id = ?;", (order_id,))
        return send_json(handler, {"success": True, "message": "Order created successfully", "order": dict(created)}, 201)

    # Update Waltz Order (via POST /api/orders/update fallback)
    if path == '/api/orders/update':
        return _update_order_internal(handler, body)

    # Delete Waltz Order (via POST /api/orders/delete fallback)
    if path == '/api/orders/delete':
        order_id = body.get('id')
        if not order_id:
            return send_json(handler, {"success": False, "error": "Order ID is required"}, 400)
        database.execute_commit("DELETE FROM waltz_orders WHERE id = ?;", (order_id,))
        return send_json(handler, {"success": True, "message": "Order deleted successfully"})

    # Create ID Invitation
    if path == '/api/directory/invitations':
        recip_name = body.get('recipient_name', '').strip()
        firm_name = body.get('firm_name', '').strip()
        email = body.get('recipient_email', '').strip()
        mobile = body.get('mobile', '').strip()
        if not recip_name or not firm_name:
            return send_json(handler, {"success": False, "error": "Recipient name and firm name required"}, 400)

        inv_code = f"NTW-INV-{uuid.uuid4().hex[:6].upper()}"
        inv_link = f"https://newtechwood.in/invite/{inv_code}"
        inv_id = f"INV-{uuid.uuid4().hex[:8]}"
        expires_at = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

        database.execute_commit("""
            INSERT INTO id_invitations (id, invitation_code, recipient_name, firm_name, recipient_email,
                                        mobile, invitation_link, status, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Active', ?);
        """, (inv_id, inv_code, recip_name, firm_name, email, mobile, inv_link, expires_at))

        created = database.execute_one("SELECT * FROM id_invitations WHERE id = ?;", (inv_id,))
        return send_json(handler, {"success": True, "message": "Invitation generated", "invitation": dict(created)}, 201)

    # Create Meeting
    if path == '/api/directory/meetings':
        firm = body.get('firm_name', '').strip()
        guest = body.get('guest_name', '').strip()
        if not firm or not guest:
            return send_json(handler, {"success": False, "error": "Firm and guest names required"}, 400)

        mtg_id = f"MTG-{uuid.uuid4().hex[:8]}"
        mtg_date = body.get('meeting_date') or datetime.now().strftime("%Y-%m-%d")
        mobile = body.get('mobile', '')
        user_type = body.get('user_type', 'New')
        guest_type = body.get('guest_type', 'Architect')
        country = body.get('country', 'India')
        state = body.get('state', 'Maharashtra')
        city = body.get('city', 'Mumbai')
        notes = body.get('discussion_notes', '')

        database.execute_commit("""
            INSERT INTO meetings (id, meeting_date, firm_name, guest_name, mobile, user_type, guest_type,
                                  country, state, city, status, discussion_notes, image_urls)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Completed', ?, '[]');
        """, (mtg_id, mtg_date, firm, guest, mobile, user_type, guest_type, country, state, city, notes))

        created = database.execute_one("SELECT * FROM meetings WHERE id = ?;", (mtg_id,))
        return send_json(handler, {"success": True, "message": "Meeting scheduled", "meeting": dict(created)}, 201)

    send_json(handler, {"error": "Endpoint not found", "path": path}, 404)

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

    database.execute_commit("""
        UPDATE waltz_orders
        SET project_name = ?, client_name = ?, status = ?, final_amount = ?,
            country = ?, state = ?, city = ?, source = ?, notes = ?
        WHERE id = ?;
    """, (proj_name, client_name, status, final_amount, country, state, city, source, notes, order_id))

    updated = database.execute_one("SELECT * FROM waltz_orders WHERE id = ?;", (order_id,))
    return send_json(handler, {"success": True, "message": "Order updated", "order": dict(updated)})

def handle_put(handler):
    parsed = urlparse(handler.path)
    path = parsed.path.rstrip('/')

    content_length = int(handler.headers.get('Content-Length', 0))
    body_bytes = handler.rfile.read(content_length) if content_length > 0 else b'{}'
    try:
        body = json.loads(body_bytes.decode('utf-8'))
    except Exception:
        body = {}

    if path == '/api/orders' or path.startswith('/api/orders/'):
        if path.startswith('/api/orders/'):
            body['id'] = path.split('/')[-1]
        return _update_order_internal(handler, body)

    send_json(handler, {"error": "Endpoint not found", "path": path}, 404)

def handle_delete(handler):
    parsed = urlparse(handler.path)
    path = parsed.path.rstrip('/')

    content_length = int(handler.headers.get('Content-Length', 0))
    body_bytes = handler.rfile.read(content_length) if content_length > 0 else b'{}'
    try:
        body = json.loads(body_bytes.decode('utf-8'))
    except Exception:
        body = {}

    if path.startswith('/api/orders/'):
        order_id = path.split('/')[-1]
        database.execute_commit("DELETE FROM waltz_orders WHERE id = ?;", (order_id,))
        return send_json(handler, {"success": True, "message": "Order deleted successfully"})

    if path == '/api/orders':
        order_id = body.get('id')
        if not order_id:
            return send_json(handler, {"success": False, "error": "Order ID is required"}, 400)
        database.execute_commit("DELETE FROM waltz_orders WHERE id = ?;", (order_id,))
        return send_json(handler, {"success": True, "message": "Order deleted successfully"})

    send_json(handler, {"error": "Endpoint not found", "path": path}, 404)

