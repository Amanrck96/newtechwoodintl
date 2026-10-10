import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1440,900")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

def set_superadmin_session(url):
    driver.get(url)
    driver.execute_script("""
        const adminUser = {
            id: 'admin',
            vendor_id: 'ADMIN-001',
            name: 'Super Administrator',
            email: 'admin@newtechwood.in',
            password: 'admin',
            role: 'superadmin',
            status: 'active',
            permissions: 'all'
        };
        localStorage.setItem('ntw_session', JSON.stringify(adminUser));
        sessionStorage.setItem('ntw_session', JSON.stringify(adminUser));
    """)
    driver.get(url)
    time.sleep(1)

try:
    print("==================================================")
    print("SUITE 1: TESTING ADMIN / VENDOR PORTAL (admin/vendor.html)")
    print("==================================================")
    set_superadmin_session("http://localhost:8000/admin/vendor.html")

    # 1. Check branding on dashboard
    print("Test 1.1: Checking Top Right Gold Button text...")
    gold_btn = driver.find_element(By.CSS_SELECTOR, "button.btn-gold[onclick*='orders']")
    btn_text = gold_btn.text
    print("Gold Button text:", repr(btn_text))
    assert "NewTechWood Orders" in btn_text, f"Expected 'NewTechWood Orders', got: {btn_text}"
    assert "Waltz" not in btn_text, f"Unexpected 'Waltz' in button: {btn_text}"

    # 1.2 Check Dashboard Tabs
    print("Test 1.2: Testing Dashboard Chart Tabs...")
    tab_amt = driver.find_element(By.ID, "btnChartProdAmount")
    tab_amt.click()
    time.sleep(0.5)
    tbl_amt = driver.find_element(By.ID, "productAmountSummaryTable")
    assert "Decking" in tbl_amt.text, "Product Amount summary table missing Decking category"

    tab_sqft = driver.find_element(By.ID, "btnChartProdSqft")
    tab_sqft.click()
    time.sleep(0.5)
    tbl_sqft = driver.find_element(By.ID, "productSqftSummaryTable")
    assert "sq.ft" in tbl_sqft.text.lower(), "Product Sq.ft summary table missing sq.ft units"

    tab_tl = driver.find_element(By.ID, "btnChartTrafficLight")
    tab_tl.click()
    time.sleep(0.5)
    tl_grid = driver.find_element(By.ID, "trafficCardsGrid")
    assert len(tl_grid.text) > 20, "Traffic Light grid empty"

    # 1.3 Check Month Filter
    print("Test 1.3: Testing Month Filter (Apr only)...")
    month_btn = driver.find_element(By.ID, "dashMonthBtn")
    month_btn.click()
    time.sleep(0.3)
    clear_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Clear')]")
    clear_btn.click()
    time.sleep(0.2)
    apr_cb = driver.find_element(By.CSS_SELECTOR, "input.dash-month-cb[value='4']")
    apr_cb.click()
    apply_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Apply Filter')]")
    apply_btn.click()
    time.sleep(0.8)
    assert "1 Selected" in month_btn.text, f"Expected 1 Selected, got: {month_btn.text}"

    # 1.4 Test Navigation to NewTechWood Orders
    print("Test 1.4: Navigating to NewTechWood Orders view...")
    gold_btn.click()
    time.sleep(0.6)
    heading = driver.find_element(By.CSS_SELECTOR, "#view-waltz-orders h1").text
    print("Orders section heading:", repr(heading))
    assert "NewTechWood Orders" in heading, f"Expected 'NewTechWood Orders', got: {heading}"
    assert "Waltz" not in heading, f"Unexpected 'Waltz' in heading: {heading}"

    # 1.5 Test Vendor Management & Access Matrix on vendor.html
    print("Test 1.5: Navigating to Vendor Account Management on vendor.html...")
    driver.execute_script("switchNav('vendors');")
    time.sleep(0.8)

    # Check "+ Create New Vendor" button
    create_vnd_btn = driver.find_element(By.ID, "btnCreateVendorHeader")
    assert create_vnd_btn.is_displayed(), "+ Create New Vendor button is not displayed!"
    print("+ Create New Vendor button is present and displayed!")

    # Check Role Access Matrix
    matrix_card = driver.find_element(By.ID, "vendorAccessMatrixCard")
    assert "Role-Based Access Control" in matrix_card.text, "RBAC Access Matrix title missing"
    assert "architect" in matrix_card.text.lower(), "Architect role missing in Access Matrix"
    assert "dealer" in matrix_card.text.lower(), "Dealer role missing in Access Matrix"
    print("Role Access Matrix verified with all partner roles!")

    # Check "+ Create New Vendor" modal
    create_vnd_btn.click()
    time.sleep(0.5)
    modal = driver.find_element(By.ID, "createVendorModal")
    assert "show" in modal.get_attribute("class"), "createVendorModal did not open"
    
    # Fill vendor modal form
    unique_email = f"selenium_{int(time.time())}@testpartners.com"
    driver.find_element(By.ID, "vendorInputFirm").send_keys("Selenium Test Partners LLP")
    driver.find_element(By.ID, "vendorInputEmail").send_keys(unique_email)
    driver.find_element(By.ID, "vendorInputPhone").send_keys("+91 98888 11223")

    # Select Dealer role
    driver.find_element(By.ID, "roleCard-dealer").click()
    time.sleep(0.3)

    # Submit form
    driver.find_element(By.ID, "btnSubmitCreateVendor").click()
    time.sleep(1.0)

    # Verify modal closed
    assert "show" not in modal.get_attribute("class"), "createVendorModal did not close after submit"
    
    # Verify vendor in table
    tbody = driver.find_element(By.ID, "vendorTableBody")
    assert "Selenium Test Partners LLP" in tbody.text, "Newly created vendor not in table"
    print("New vendor created and verified in active directory table!")

    # Screenshot vendor portal
    driver.save_screenshot("artifacts/vendor_portal_verified_suite.png")
    print("Saved screenshot: artifacts/vendor_portal_verified_suite.png")

    print("\n==================================================")
    print("SUITE 2: TESTING ROOT ADMIN PORTAL (admin.html)")
    print("==================================================")
    set_superadmin_session("http://localhost:8000/admin.html")

    # Check gold button on admin.html
    admin_gold = driver.find_element(By.CSS_SELECTOR, "button.btn-gold[onclick*='orders']")
    assert "NewTechWood Orders" in admin_gold.text
    assert "Waltz" not in admin_gold.text

    # Check vendor management on admin.html
    driver.execute_script("switchNav('vendors');")
    time.sleep(0.6)
    admin_create_vnd = driver.find_element(By.ID, "btnCreateVendorHeader")
    assert admin_create_vnd.is_displayed()
    admin_matrix = driver.find_element(By.ID, "vendorAccessMatrixCard")
    assert "Role-Based Access Control" in admin_matrix.text
    print("Admin portal vendor management verified!")

    driver.save_screenshot("artifacts/admin_portal_verified_suite.png")
    print("Saved screenshot: artifacts/admin_portal_verified_suite.png")

    # Check toasts for any errors
    toasts = driver.find_elements(By.CSS_SELECTOR, ".toast.toast-error")
    assert len(toasts) == 0, f"Found unexpected error toasts: {[t.text for t in toasts]}"
    print("Zero error toasts detected across entire test run!")

    print("\nALL AUTOMATED TESTS PASSED WITH 100% SUCCESS!")

finally:
    driver.quit()
