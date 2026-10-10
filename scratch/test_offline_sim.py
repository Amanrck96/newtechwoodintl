import time, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')
options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)
try:
    driver.get('http://127.0.0.1:8000/admin/')
    time.sleep(1)
    if '/login' in driver.current_url:
        driver.find_element(By.ID, 'loginEmail').send_keys('admin')
        driver.find_element(By.ID, 'loginPassword').send_keys('admin')
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

    # Force network failure
    driver.execute_script("""
        window.fetch = function() {
            return Promise.reject(new Error('Simulated network offline'));
        };
        dashState.data = null;
        loadDashboardData();
    """)
    time.sleep(1)

    pipe_val = driver.find_element(By.ID, 'kpiDashPipeValue').text.strip()
    pipe_count = driver.find_element(By.ID, 'kpiDashPipeCount').text.strip()
    print('Offline Fallback KPIs:', pipe_val, f'({pipe_count} deals)')
    assert pipe_count != '0' and pipe_val != '₹0 Cr', 'Offline fallback should compute valid KPIs!'

    # Test tab switching in offline mode
    driver.find_element(By.ID, 'btnChartProdAmount').click()
    time.sleep(0.5)
    amt_text = driver.find_element(By.ID, 'productAmountSummaryTable').text.strip()
    assert 'UltraShield Decking' in amt_text, 'Offline product breakdown should work!'
    print('OFFLINE SIMULATION 100% PASSED!')
finally:
    driver.quit()
