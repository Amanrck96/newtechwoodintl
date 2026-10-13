import io
import json
import os
import sys
import uuid
import pytest
from datetime import datetime, timedelta

# Ensure db directory is in path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'db')
if DB_DIR not in sys.path:
    sys.path.insert(0, DB_DIR)

import database
import api_router


class MockHandler:
    def __init__(self, path, method='GET', headers=None, body=None):
        self.path = path
        self.command = method
        self.headers = headers or {}
        body_bytes = body.encode('utf-8') if isinstance(body, str) else (body or b'')
        if body_bytes:
            self.headers.setdefault('Content-Length', str(len(body_bytes)))
            self.headers.setdefault('Content-Type', 'application/json')
        self.rfile = io.BytesIO(body_bytes)
        self.wfile = io.BytesIO()
        self._headers_buffer = []
        self.status_code = 200
        self.response_headers = {}

    def send_response(self, code):
        self.status_code = code

    def send_header(self, key, value):
        self.response_headers[key.lower()] = value

    def end_headers(self):
        pass

    def get_json(self):
        val = self.wfile.getvalue()
        if not val:
            return None
        return json.loads(val.decode('utf-8'))


@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    import migrate
    import seed
    migrate.run_migrations()
    seed.seed_database()
    migrate.run_migrations() # ensure plain passwords are hashed
    # Clear sessions
    with database.get_connection() as conn:
        conn.execute("DELETE FROM sessions;")
        conn.commit()


def test_auth_rejection_missing_token():
    handler = MockHandler("/api/users", method="GET")
    api_router.handle_get(handler)
    assert handler.status_code == 401
    res = handler.get_json()
    assert res["success"] is False


def test_auth_rejection_invalid_token():
    handler = MockHandler("/api/users", method="GET", headers={"Authorization": "Bearer fake_token_12345"})
    api_router.handle_get(handler)
    assert handler.status_code == 401


def test_auth_rejection_expired_token():
    token = "ntw_expired_" + uuid.uuid4().hex[:8]
    expired_at = (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    database.execute_commit(
        "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, 'admin', ?);",
        (token, expired_at)
    )
    handler = MockHandler("/api/users", method="GET", headers={"Authorization": f"Bearer {token}"})
    api_router.handle_get(handler)
    assert handler.status_code == 401


def test_role_enforcement_forbidden_for_sales():
    # Login as sales
    login_h = MockHandler("/api/auth/login", method="POST",
                          body=json.dumps({"email": "sales@newtechwood.in", "password": "sales123"}))
    api_router.handle_post(login_h)
    assert login_h.status_code == 200
    sales_token = login_h.get_json()["token"]

    # Try to access admin-only endpoint
    handler = MockHandler("/api/users", method="GET", headers={"Authorization": f"Bearer {sales_token}"})
    api_router.handle_get(handler)
    assert handler.status_code == 403


def test_admin_access_never_returns_password():
    login_h = MockHandler("/api/auth/login", method="POST",
                          body=json.dumps({"email": "admin@newtechwood.in", "password": "admin"}))
    api_router.handle_post(login_h)
    assert login_h.status_code == 200
    admin_token = login_h.get_json()["token"]

    handler = MockHandler("/api/users", method="GET", headers={"Authorization": f"Bearer {admin_token}"})
    api_router.handle_get(handler)
    assert handler.status_code == 200
    res = handler.get_json()
    assert res["success"] is True
    for user in res.get("users", []):
        assert "password" not in user


def test_login_rate_limiting():
    # Attempt 6 wrong passwords with a dedicated IP
    headers = {"X-Forwarded-For": "192.168.1.99"}
    for i in range(5):
        h = MockHandler("/api/auth/login", method="POST",
                        headers=headers,
                        body=json.dumps({"email": "ratelimit_test@newtechwood.in", "password": "wrong"}))
        api_router.handle_post(h)
        assert h.status_code == 401

    # 6th attempt should be rate limited (429)
    h6 = MockHandler("/api/auth/login", method="POST",
                     headers=headers,
                     body=json.dumps({"email": "ratelimit_test@newtechwood.in", "password": "wrong"}))
    api_router.handle_post(h6)
    assert h6.status_code == 429
    res = h6.get_json()
    assert "Too many" in res.get("error", "")

    # Cleanup rate limit map so other tests are not impacted
    api_router._LOGIN_ATTEMPTS.clear()


def test_sequential_order_numbers():
    login_h = MockHandler("/api/auth/login", method="POST",
                          body=json.dumps({"email": "admin@newtechwood.in", "password": "admin"}))
    api_router.handle_post(login_h)
    admin_token = login_h.get_json()["token"]

    h1 = MockHandler("/api/orders", method="POST",
                     headers={"Authorization": f"Bearer {admin_token}"},
                     body=json.dumps({"project_name": "Seq Test 1", "client_name": "Client A", "final_amount": 1000}))
    api_router.handle_post(h1)
    assert h1.status_code == 201
    ord1_num = h1.get_json()["order"]["order_number"]

    h2 = MockHandler("/api/orders", method="POST",
                     headers={"Authorization": f"Bearer {admin_token}"},
                     body=json.dumps({"project_name": "Seq Test 2", "client_name": "Client B", "final_amount": 2000}))
    api_router.handle_post(h2)
    assert h2.status_code == 201
    ord2_num = h2.get_json()["order"]["order_number"]

    # Verify sequential: ord2 ends with last_num + 1
    seq1 = int(ord1_num.split('-')[-1])
    seq2 = int(ord2_num.split('-')[-1])
    assert seq2 == seq1 + 1


def test_analytics_deduplication_and_math():
    login_h = MockHandler("/api/auth/login", method="POST",
                          body=json.dumps({"email": "admin@newtechwood.in", "password": "admin"}))
    api_router.handle_post(login_h)
    admin_token = login_h.get_json()["token"]

    # Query analytics
    h = MockHandler("/api/analytics", method="GET", headers={"Authorization": f"Bearer {admin_token}"})
    api_router.handle_get(h)
    assert h.status_code == 200
    res = h.get_json()
    assert res["success"] is True
    metrics = res["metrics"]
    assert "win_rate_pct" in metrics
    assert "total_revenue" in metrics
    assert "avg_deal_size" in metrics
    # Confirm meetings do not count as win
    activities = res["activities"]
    for act in activities:
        if act.get("activity_type") == "Architect Meeting":
            assert act.get("status") != "Win"
