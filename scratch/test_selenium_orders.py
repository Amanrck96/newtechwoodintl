import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1440,900')

driver = webdriver.Chrome(options=options)
try:
    print("Navigating to http://127.0.0.1:8000/admin/...")
    driver.get("http://127.0.0.1:8000/admin/")
    time.sleep(1)

    if "/login" in driver.current_url:
        print("Logging in as admin...")
        driver.find_element(By.ID, "loginEmail").send_keys("admin")
        driver.find_element(By.ID, "loginPassword").send_keys("admin")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

    # 1. Check Executive Dashboard top button
    btn_orders = driver.find_element(By.CSS_SELECTOR, "#view-dashboard .btn-gold")
    btn_text = btn_orders.get_attribute("textContent").strip()
    print("Dashboard top gold button textContent:", repr(btn_text))
    assert "NewTechWood Orders" in btn_text, f"Expected 'NewTechWood Orders' on button, got: {btn_text}"
    assert "Waltz" not in btn_text, f"Unexpected 'Waltz' in button: {btn_text}"

    # Take screenshot of Dashboard with the NewTechWood Orders button clearly visible
    os.makedirs("artifacts", exist_ok=True)
    driver.save_screenshot("artifacts/dashboard_newtech_orders_verified.png")
    print("Saved screenshot to artifacts/dashboard_newtech_orders_verified.png")

    # 2. Click the NewTechWood Orders button
    btn_orders.click()
    time.sleep(1)

    # Check section title
    heading_el = driver.find_element(By.CSS_SELECTOR, "#view-waltz-orders h1")
    heading = heading_el.get_attribute("textContent").strip()
    print("Orders view heading textContent:", repr(heading))
    assert heading == "NewTechWood Orders", f"Expected 'NewTechWood Orders', got: {heading}"
    assert "Waltz" not in heading, f"Unexpected 'Waltz' in heading: {heading}"

    driver.save_screenshot("artifacts/orders_view_newtech_verified.png")
    print("Saved screenshot to artifacts/orders_view_newtech_verified.png")

    # 3. Check sidebar label
    nav_link = driver.find_element(By.ID, "nav-waltz")
    sidebar_label = nav_link.get_attribute("textContent").strip()
    print("Sidebar nav link textContent:", repr(sidebar_label))
    assert "NewTechWood Orders" in sidebar_label, f"Expected 'NewTechWood Orders' in sidebar label, got: {sidebar_label}"
    assert "Waltz" not in sidebar_label, f"Unexpected 'Waltz' in sidebar label: {sidebar_label}"

    print("\nALL NEWTECHWOOD BRANDING VERIFICATIONS PASSED SUCCESSFULLY!")

finally:
    driver.quit()
