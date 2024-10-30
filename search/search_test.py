#cd search

#---Batch Execution
#pytest -v

#---Individual Execution---
#pytest -k "test_case_01" search_test.py
#pytest -k "test_case_02" search_test.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(params=["chrome", "edge"])
def driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "edge":
        driver = webdriver.Edge()

    driver.get("http://www.automationpractice.pl/index.php")
    driver.maximize_window()
    yield driver
    driver.quit()

# TC01: Kiểm tra tìm kiếm đúng kết quả.
def test_case_01(driver):
    driver.find_element(By.ID, "search_query_top").send_keys("dresses")
    driver.find_element(By.NAME, "submit_search").click()

    search_keyword = WebDriverWait(driver, 12).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.page-heading .lighter"))
    )
    assert search_keyword.text == '"DRESSES"' or None

# TC02: Kiểm tra tìm kiếm sai kết quả.
def test_case_02(driver):
    driver.find_element(By.ID, "search_query_top").send_keys("abc")
    driver.find_element(By.NAME, "submit_search").click()

    search_keyword = WebDriverWait(driver, 12).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.alert"))
    )
    assert search_keyword.text == 'No results were found for your search "abc"' or None




