"""
E2E Playwright Browser Test Suite for NewTechWood India CRM & Vendor Portal
Verifies:
1. Login flow as Admin & as Vendor
2. Complete Vendor <-> Admin Request Lifecycle (Create -> Inbox -> In Review -> Quoted -> Reply)
3. Vendor 360 profile & metrics view
4. Zero uncaught console errors throughout execution
"""

import os
import sys
import time
import subprocess
import sqlite3
import pytest
import bcrypt
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(TEST_DIR)
E2E_DB = os.path.join(PROJECT_DIR, "db", "test_e2e_crm.db")
SERVER_PORT = 8011
BASE_URL = f"http://127.0.0.1:{SERVER_PORT}"


def setup_e2e_database():
    """Initializes a fresh SQLite database, applies all migrations, and seeds users."""
    if os.path.exists(E2E_DB):
        try:
            os.remove(E2E_DB)
        except OSError:
            pass

    try:
        from db import migrate
    except ImportError:
        import migrate
    migrate.run_migrations(db_path=E2E_DB)

    conn = sqlite3.connect(E2E_DB)
    cur = conn.cursor()

    # Seed Admin User
    admin_hash = bcrypt.hashpw(b"admin_pass_123!", bcrypt.gensalt()).decode("utf-8")
    cur.execute("""
        INSERT INTO users (id, email, password, full_name, role, status, permissions)
        VALUES ('admin', 'admin@newtechwood.in', ?, 'Super Administrator', 'admin', 'active', 'all')
    """, (admin_hash,))

    # Seed Vendor (Architect) User
    vendor_hash = bcrypt.hashpw(b"arch_pass_123!", bcrypt.gensalt()).decode("utf-8")
    cur.execute("""
        INSERT INTO users (id, email, password, full_name, role, status, permissions, vendor_id, phone)
        VALUES ('arch_demo', 'architect@designstudio.in', ?, 'Ar. Rohan Mehta', 'architect', 'active', 'gopro_cad,pipeline_specs,meetings,invitations', 'VND-ARCH-01', '+91 98200 12345')
    """, (vendor_hash,))

    # Seed Product for catalog
    cur.execute("""
        INSERT INTO products (id, sl_no, name, code, category, item_type, price, dealer_price, architect_price, price_unit, gst_extra, gst_pct, dimensions, length_mm, width_mm, thickness_mm, status)
        VALUES ('p_deck_01', 1, 'UltraShield Composite Decking', 'UH02', 'Decking', 'main', 420.0, 360.0, 380.0, 'SFT', 1, 18.0, '23mm x 138mm x 2800mm', 2800, 138, 23, 'active')
    """)

    conn.commit()
    conn.close()


@pytest.fixture(scope="module")
def web_server():
    """Starts serve.py background process on port 8011 using test database."""
    setup_e2e_database()

    env = os.environ.copy()
    env["CRM_DB_FILE"] = E2E_DB
    env["PORT"] = str(SERVER_PORT)

    # Start serve.py with modified port
    server_code = f"""
import sys, os
sys.path.insert(0, r"{PROJECT_DIR}")
import serve
serve.PORT = {SERVER_PORT}
import http.server, socketserver
handler = serve.RangeRequestHandler
with serve.ThreadingTCPServer(("", {SERVER_PORT}), handler) as httpd:
    print(f"Serving at port {SERVER_PORT}")
    httpd.serve_forever()
"""
    proc = subprocess.Popen(
        [sys.executable, "-c", server_code],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for server to bind
    time.sleep(1.5)
    yield BASE_URL

    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()


def get_playwright_browser(p):
    """Launches system installed Edge or Chrome."""
    try:
        return p.chromium.launch(headless=True, channel="msedge")
    except Exception:
        return p.chromium.launch(headless=True, channel="chrome")


def test_complete_request_lifecycle_and_zero_console_errors(web_server):
    """
    Full end-to-end user journey test:
    1. Vendor logs in -> Submits request -> sees it in Tracker
    2. Admin logs in -> Views inbox -> Updates status -> Posts comments
    3. Vendor sees update -> Posts reply
    4. Admin views Vendor 360
    5. Zero console errors throughout
    """
    console_errors = []

    def handle_console_msg(msg):
        if msg.type == "error":
            # Ignore 404 for favicon if any
            if "favicon" not in msg.text.lower():
                console_errors.append(f"Console error: {msg.text}")

    def handle_page_error(err):
        console_errors.append(f"Uncaught page exception: {err}")

    with sync_playwright() as p:
        browser = get_playwright_browser(p)

        # ==========================================================
        # STEP 1: VENDOR LOGIN & SUBMIT REQUEST
        # ==========================================================
        vendor_ctx = browser.new_context()
        v_page = vendor_ctx.new_page()

        def log_console(msg):
            print(f"[BROWSER {msg.type.upper()}] {msg.text}")
            if msg.type == "error" and "favicon" not in msg.text.lower():
                console_errors.append(msg.text)

        v_page.on("console", log_console)
        v_page.on("pageerror", handle_page_error)
        v_page.on("dialog", lambda d: (print(f"[DIALOG] {d.message}"), d.accept()))

        # Navigate to login
        v_page.goto(f"{BASE_URL}/login/index.html")
        assert "Sign In" in v_page.title()

        # Login as Architect
        v_page.fill("#loginEmail", "arch_demo")
        v_page.fill("#loginPassword", "arch_pass_123!")
        v_page.click("button.btn-submit")

        # Expect redirect to vendor portal
        v_page.wait_for_url("**/admin/vendor.html", timeout=6000)
        assert "Partner & Vendor Portal" in v_page.title()
        v_page.wait_for_selector("#vview-dashboard", state="visible")

        # Open New Request modal
        v_page.click("button.btn-new-req")
        v_page.wait_for_selector("#newRequestModal.show", state="visible")

        # Fill request details
        v_page.select_option("#newReqType", "Quote / price request")
        v_page.fill("#newReqTitle", "E2E Pune Penthouse Decking BOQ")
        v_page.select_option("#newReqPriority", "Urgent")
        v_page.fill("#newReqDetails", "Need sample boards and quote for 450 Sq.ft of UltraShield teak decking.")

        v_page.click("#btnSubmitReq")

        # Wait for modal to close (becomes hidden)
        v_page.wait_for_selector("#newRequestModal", state="hidden")

        # Switch to My Requests
        v_page.click("#vnav-requests")
        v_page.wait_for_selector("#vendorReqTableBody:has-text('E2E Pune Penthouse Decking BOQ')", timeout=6000)
        table_text = v_page.inner_text("#vendorReqTableBody")
        assert "E2E Pune Penthouse Decking BOQ" in table_text
        assert "urgent" in table_text.lower()
        assert "New" in table_text

        # ==========================================================
        # STEP 2: ADMIN INBOX & STATUS WORKFLOW
        # ==========================================================
        admin_ctx = browser.new_context()
        a_page = admin_ctx.new_page()
        a_page.on("console", handle_console_msg)
        a_page.on("pageerror", handle_page_error)
        a_page.on("dialog", lambda d: (print(f"[ADMIN DIALOG] {d.message}"), d.accept()))

        a_page.goto(f"{BASE_URL}/login/index.html")
        a_page.fill("#loginEmail", "admin")
        a_page.fill("#loginPassword", "admin_pass_123!")
        a_page.click("button.btn-submit")

        # Admin lands on admin portal
        a_page.wait_for_url("**/admin/", timeout=6000)
        a_page.wait_for_selector("#view-dashboard", state="visible")

        # Navigate to Request Inbox
        a_page.click("#nav-vendor-inbox")
        a_page.wait_for_selector("#inboxTableBody:has-text('E2E Pune Penthouse Decking BOQ')", timeout=6000)
        inbox_text = a_page.inner_text("#inboxTableBody")
        assert "E2E Pune Penthouse Decking BOQ" in inbox_text
        assert "Ar. Rohan Mehta" in inbox_text

        # Click Manage on the request
        a_page.click("#inboxTableBody tr button:has-text('Manage')")
        a_page.wait_for_selector("#requestDetailModal.show", state="visible")

        # Update status to 'In Review'
        a_page.select_option("#reqUpdateStatusSelect", "In Review")
        a_page.click("button:has-text('Update Status')")
        a_page.wait_for_selector("#reqActivityTimeline:has-text('Status updated to In Review')", timeout=15000)

        # Post an admin reply
        a_page.fill("#reqCommentText", "Technical team is evaluating the terrace BOQ requirements.")
        a_page.click("button:has-text('Submit Reply')")
        a_page.wait_for_selector("#reqActivityTimeline:has-text('Technical team is evaluating the terrace BOQ requirements.')", timeout=15000)

        # Update status to 'Quoted/Approved'
        a_page.select_option("#reqUpdateStatusSelect", "Quoted/Approved")
        a_page.click("button:has-text('Update Status')")
        a_page.wait_for_selector("#reqActivityTimeline:has-text('Status updated to Quoted/Approved')", timeout=15000)

        # Close detail modal
        a_page.click("#requestDetailModal .modal-close-btn")
        a_page.wait_for_selector("#requestDetailModal", state="hidden")

        # Check Vendor 360 View
        a_page.click("#nav-vendors")
        a_page.wait_for_selector("#vendorTableBody tr:has-text('Ar. Rohan Mehta')", timeout=15000)
        a_page.click("#vendorTableBody tr:has-text('Ar. Rohan Mehta') button:has-text('Vendor 360')")
        a_page.wait_for_selector("#vendor360Modal.show", state="visible")
        a_page.wait_for_selector("#vendor360Modal:has-text('Ar. Rohan Mehta')", timeout=15000)
        v360_text = a_page.inner_text("#vendor360Modal")
        assert "Ar. Rohan Mehta" in v360_text
        assert "VND-ARCH-01" in v360_text
        a_page.click("#vendor360Modal .modal-close-btn")
        a_page.wait_for_selector("#vendor360Modal", state="hidden")

        # ==========================================================
        # STEP 3: VENDOR VERIFIES UPDATE & REPLIES
        # ==========================================================
        v_page.bring_to_front()
        v_page.click("#vnav-requests")
        v_page.wait_for_selector("#vendorReqTableBody:has-text('Quoted/Approved')", timeout=6000)
        req_row = v_page.inner_text("#vendorReqTableBody")
        assert "Quoted/Approved" in req_row

        # Open Timeline
        v_page.click("#vendorReqTableBody button:has-text('View Timeline')")
        v_page.wait_for_selector("#viewReqTimelineModal.show", state="visible")
        v_page.wait_for_selector("#timelineModalBody:has-text('Technical team is evaluating the terrace BOQ requirements.')", timeout=6000)

        # Vendor replies back
        v_page.fill("#vendorReplyText", "Confirmed! Please proceed with sample delivery to our studio.")
        v_page.click("button:has-text('Send Reply')")
        v_page.wait_for_selector("#timelineModalBody:has-text('Confirmed! Please proceed with sample delivery')", timeout=12000)
        v_page.click("#viewReqTimelineModal .modal-close-btn")
        v_page.wait_for_selector("#viewReqTimelineModal", state="hidden")

        # Check Catalog & Price Tier
        v_page.click("#vnav-catalog")
        v_page.wait_for_selector("#catalogTableBody tr:has-text('UltraShield Composite Decking')", timeout=10000)
        cat_text = v_page.inner_text("#catalogTableBody")
        assert "UltraShield Composite Decking" in cat_text
        # Architect price is 380
        assert "380" in cat_text

        # ==========================================================
        # STEP 4: VERIFY ZERO CONSOLE ERRORS
        # ==========================================================
        vendor_ctx.close()
        admin_ctx.close()
        browser.close()

    print(f"Total console errors captured: {len(console_errors)}")
    if console_errors:
        print("Captured errors:", console_errors)
    assert len(console_errors) == 0, f"Expected 0 console errors, but got: {console_errors}"
