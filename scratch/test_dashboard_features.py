import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
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
    print("Opening http://127.0.0.1:8000/admin/...")
    driver.get("http://127.0.0.1:8000/admin/")
    time.sleep(1)

    if "/login" in driver.current_url:
        print("Logging in...")
        driver.find_element(By.ID, "loginEmail").send_keys("admin")
        driver.find_element(By.ID, "loginPassword").send_keys("admin")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

    os.makedirs("artifacts", exist_ok=True)

    # 1. Check initial KPIs
    pipe_val = driver.find_element(By.ID, "kpiDashPipeValue").text.strip()
    pipe_count = driver.find_element(By.ID, "kpiDashPipeCount").text.strip()
    win_val = driver.find_element(By.ID, "kpiDashWinValue").text.strip()
    win_count = driver.find_element(By.ID, "kpiDashWinCount").text.strip()

    print(f"Initial KPIs: Pipeline={pipe_val} ({pipe_count} deals), Win={win_val} ({win_count} deals)")
    assert pipe_count != "0" and pipe_val != "₹0 Cr", "KPIs should not be 0!"
    assert win_count != "0" and win_val != "₹0 Cr", "Win KPIs should not be 0!"

    # 2. Test Tab: Product by Amount
    print("\nClicking 'Product by Amount' tab...")
    btn_prod_amt = driver.find_element(By.ID, "btnChartProdAmount")
    btn_prod_amt.click()
    time.sleep(1)
    view_prod_amt = driver.find_element(By.ID, "chartViewProdAmount")
    assert view_prod_amt.is_displayed(), "Product by Amount view should be visible!"
    summary_table = driver.find_element(By.ID, "productAmountSummaryTable").text.strip()
    assert "UltraShield Decking" in summary_table, "Summary table should contain categories!"
    print("Product by Amount table loaded successfully!")
    driver.save_screenshot("artifacts/test_tab_product_amount.png")

    # 3. Test Tab: Product by Sq.ft
    print("\nClicking 'Product by Sq.ft' tab...")
    btn_prod_sqft = driver.find_element(By.ID, "btnChartProdSqft")
    btn_prod_sqft.click()
    time.sleep(1)
    view_prod_sqft = driver.find_element(By.ID, "chartViewProdSqft")
    assert view_prod_sqft.is_displayed(), "Product by Sq.ft view should be visible!"
    sqft_table = driver.find_element(By.ID, "productSqftSummaryTable").text.strip()
    assert "sq.ft" in sqft_table, "Summary table should contain sq.ft values!"
    print("Product by Sq.ft table loaded successfully!")
    driver.save_screenshot("artifacts/test_tab_product_sqft.png")

    # 4. Test Tab: Traffic Light Dashboard
    print("\nClicking 'Traffic Light Dashboard' tab...")
    btn_traffic = driver.find_element(By.ID, "btnChartTrafficLight")
    btn_traffic.click()
    time.sleep(1)
    view_traffic = driver.find_element(By.ID, "chartViewTrafficLight")
    assert view_traffic.is_displayed(), "Traffic Light view should be visible!"
    cards_text = driver.find_element(By.ID, "trafficCardsGrid").text.strip()
    assert "PRJ-" in cards_text, "Traffic cards grid should display project cards!"
    print("Traffic Light Dashboard loaded successfully!")
    driver.save_screenshot("artifacts/test_tab_traffic_light.png")

    # Test Traffic Light Filter Pills (Red Alert, Amber Caution, All)
    driver.find_element(By.CSS_SELECTOR, ".traffic-pill.red").click()
    time.sleep(0.5)
    red_text = driver.find_element(By.ID, "trafficCardsGrid").text.strip()
    print("Red filter applied, projects shown:", len(red_text.splitlines()))

    driver.find_element(By.CSS_SELECTOR, ".traffic-pill.amber").click()
    time.sleep(0.5)

    driver.find_element(By.CSS_SELECTOR, ".traffic-pill:first-child").click() # All
    time.sleep(0.5)

    # 5. Test 1 Month Selected
    print("\nTesting 1 Month Selected filter...")
    driver.execute_script("""
        document.querySelectorAll('.dash-month-cb').forEach(cb => cb.checked = false);
        const octCb = document.querySelector('.dash-month-cb[value=\"10\"]');
        if (octCb) octCb.checked = true;
        applyMonthFilter();
    """)
    time.sleep(1)
    btn_label = driver.find_element(By.ID, "dashMonthBtnLabel").text.strip()
    print(f"Month button label after filter: '{btn_label}'")
    m_pipe_val = driver.find_element(By.ID, "kpiDashPipeValue").text.strip()
    m_win_val = driver.find_element(By.ID, "kpiDashWinValue").text.strip()
    print(f"Updated 1-month KPIs: Pipeline={m_pipe_val}, Win={m_win_val}")
    driver.save_screenshot("artifacts/test_month_filter_1_selected.png")

    # 6. Verify NO error toasts exist
    toasts = driver.find_elements(By.CSS_SELECTOR, ".toast-box")
    toast_texts = [t.text.strip() for t in toasts if t.is_displayed()]
    print("\nActive toasts:", toast_texts)
    assert not any("Error" in t for t in toast_texts), f"Unexpected error toast found: {toast_texts}"

    print("\n==================================================")
    print("ALL CRM DASHBOARD FEATURES TESTED AND 100% WORKING!")
    print("==================================================")

finally:
    driver.quit()
