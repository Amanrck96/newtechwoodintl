import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1440,900')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
try:
    driver.get("http://127.0.0.1:8000/admin/")
    time.sleep(1)

    if "/login" in driver.current_url:
        driver.find_element(By.ID, "loginEmail").send_keys("admin")
        driver.find_element(By.ID, "loginPassword").send_keys("admin")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

    print("Current URL:", driver.current_url)

    # Print all browser console logs
    logs = driver.get_log('browser')
    print("\n--- BROWSER CONSOLE LOGS ON LOAD ---")
    for log in logs:
        print(f"[{log['level']}] {log['message']}")

    # Now click each chart button and print console logs
    for btn_id in ['btnChartProdAmount', 'btnChartProdSqft', 'btnChartTrafficLight']:
        btn = driver.find_element(By.ID, btn_id)
        btn.click()
        time.sleep(1)
        logs = driver.get_log('browser')
        print(f"\n--- LOGS AFTER CLICKING {btn_id} ---")
        for log in logs:
            print(f"[{log['level']}] {log['message']}")

    # Now change month to 1 selected
    driver.execute_script("""
        dashState.selectedMonths = [1];
        loadDashboardData();
    """)
    time.sleep(1)
    logs = driver.get_log('browser')
    print("\n--- LOGS AFTER SELECTING 1 MONTH ---")
    for log in logs:
        print(f"[{log['level']}] {log['message']}")

finally:
    driver.quit()
