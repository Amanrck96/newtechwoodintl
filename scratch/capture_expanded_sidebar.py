import time
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
    driver.get("http://127.0.0.1:8000/admin/")
    time.sleep(1)

    if "/login" in driver.current_url:
        driver.find_element(By.ID, "loginEmail").send_keys("admin")
        driver.find_element(By.ID, "loginPassword").send_keys("admin")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

    # Expand sidebar using toggleSidebar()
    driver.execute_script("toggleSidebar();")
    time.sleep(1)

    # Take screenshot of expanded sidebar
    driver.save_screenshot("artifacts/sidebar_expanded_verified.png")
    print("Screenshot saved to artifacts/sidebar_expanded_verified.png")

finally:
    driver.quit()
