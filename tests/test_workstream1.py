import io
import json
import os
import sys
import uuid
import pytest
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'db')
if DB_DIR not in sys.path:
    sys.path.insert(0, DB_DIR)

import database
import api_router
import products_api
import migrate
import seed_products


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
def setup_products():
    os.environ.pop("CRM_DB_FILE", None)
    migrate.run_migrations()
    seed_products.seed(reset=True)


def test_quote_calculation_maths():
    """P1: Verify quote formulas.
    Twix PRD-001: 2900mm x 200mm = 0.58 m2 = 6.243 sft plank area.
    Price = Rs 850 / SFT (+ 18% GST).
    Clip PRD-005: 7 clips per plank at Rs 35 / clip (+ 18% GST).
    """
    items = [{"product_id": "PRD-001", "area_sft": 100.0, "wastage_pct": 10.0}]
    quote = products_api.calculate_quote(items)
    assert "lines" in quote
    assert len(quote["lines"]) == 2  # main product + auto clip accessory

    main_line = quote["lines"][0]
    clip_line = quote["lines"][1]

    assert main_line["product_id"] == "PRD-001"
    # Planks calculation: ceil(100 * 1.10 / 6.24307) = ceil(17.619) = 18 planks
    assert main_line["planks"] == 18
    # Billed sft = 18 * 6.24307 = ~112.38 sft
    assert main_line["billed_sft"] > 100.0
    # Amount = billed_sft * 850
    expected_amount = round(main_line["billed_sft"] * 850.0, 2)
    assert abs(main_line["amount"] - expected_amount) < 0.05

    # Clip calculation: 18 planks * 7 clips/plank = 126 clips
    assert clip_line["qty"] == 126
    assert clip_line["amount"] == 126 * 35.0

    # Total check
    assert quote["subtotal"] == round(main_line["amount"] + clip_line["amount"], 2)
    assert quote["gst"] == round(quote["subtotal"] * 0.18, 2)
    assert quote["total"] == round(quote["subtotal"] + quote["gst"], 2)


def test_dealer_and_architect_price_tiers():
    """P4: Verify tier pricing."""
    # Architect tier
    p_arch = products_api.get_product_for_tier("PRD-001", tier="architect")
    assert p_arch["effective_price"] == 722.50

    # Dealer tier
    p_dlr = products_api.get_product_for_tier("PRD-001", tier="dealer")
    assert p_dlr["effective_price"] == 765.00


def test_link_products_to_orders():
    """P2: Verify creating an order with order lines and calculating final_amount."""
    login_h = MockHandler("/api/auth/login", method="POST",
                          body=json.dumps({"email": "admin@newtechwood.in", "password": "admin"}))
    api_router.handle_post(login_h)
    admin_token = login_h.get_json()["token"]

    order_payload = {
        "project_name": "Villa Decking Goa",
        "client_name": "Goa Resorts Pvt Ltd",
        "order_lines": [
            {"product_id": "PRD-006", "variant_color": "Teak", "area_sft": 50.0, "wastage_pct": 10.0},
            {"product_id": "PRD-004", "variant_color": "Teak", "qty": 4}
        ]
    }
    h = MockHandler("/api/orders", method="POST",
                    headers={"Authorization": f"Bearer {admin_token}"},
                    body=json.dumps(order_payload))
    api_router.handle_post(h)
    assert h.status_code == 201
    res = h.get_json()
    assert res["success"] is True
    order = res["order"]
    assert order["final_amount"] > 0

    # Verify order lines were stored in database
    lines = database.execute_query("SELECT * FROM order_lines WHERE order_id = ?;", (order["id"],))
    assert len(lines) >= 2


def test_product_chart_aggregation():
    """P3: Verify dashboard product chart categories feed."""
    login_h = MockHandler("/api/auth/login", method="POST",
                          body=json.dumps({"email": "admin@newtechwood.in", "password": "admin"}))
    api_router.handle_post(login_h)
    admin_token = login_h.get_json()["token"]

    h = MockHandler("/api/products/chart", method="GET", headers={"Authorization": f"Bearer {admin_token}"})
    api_router.handle_get(h)
    assert h.status_code == 200
    res = h.get_json()
    assert res["success"] is True
    assert "categories" in res
    assert "by_amount" in res
    assert "by_sqft" in res


def test_quote_conversion_to_pipeline_project():
    """P5: Convert quote to pipeline project."""
    login_h = MockHandler("/api/auth/login", method="POST",
                          body=json.dumps({"email": "admin@newtechwood.in", "password": "admin"}))
    api_router.handle_post(login_h)
    admin_token = login_h.get_json()["token"]

    convert_payload = {
        "type": "pipeline",
        "project_name": "Oberoi Commercial Decking",
        "client_name": "Oberoi Constructions",
        "items": [{"product_id": "PRD-006", "area_sft": 200.0, "wastage_pct": 10.0}]
    }
    h = MockHandler("/api/products/quote/convert", method="POST",
                    headers={"Authorization": f"Bearer {admin_token}"},
                    body=json.dumps(convert_payload))
    api_router.handle_post(h)
    assert h.status_code == 201
    res = h.get_json()
    assert res["success"] is True
    assert "project_id" in res


def test_excel_bulk_import():
    """P6: Bulk import / update from PPT - TECHWOOD (1).xlsx."""
    excel_path = r"C:\Users\amanr\Downloads\PPT - TECHWOOD (1).xlsx"
    assert os.path.exists(excel_path)
    result = products_api.import_products_from_excel(excel_path, commit=True)
    assert result["success"] is True
    assert result["imported_count"] >= 9
