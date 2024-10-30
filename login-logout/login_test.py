#cd login-logout

#---Batch Execution---
#pytest -v

#---Individual Execution---
#pytest -k "test_case_01" login_test.py
#pytest -k "test_case_02" login_test.py
#pytest -k "test_case_03" login_test.py
#pytest -k "test_case_04" login_test.py
#pytest -k "test_case_05" login_test.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest


@pytest.fixture(params=["chrome", "edge"])
def driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "edge":
        driver = webdriver.Edge()
        
    driver.get("http://www.automationpractice.pl/index.php?controller=authentication&back=my-account")
    driver.maximize_window()
    yield driver
    driver.quit()


#TC01: Kiểm tra đăng nhập thành công.
def test_case_01(driver):
    driver.find_element(By.ID, "email").send_keys("ndtai0912@gmail.com")
    driver.find_element(By.ID, "passwd").send_keys("abc123")
    driver.find_element(By.ID, "SubmitLogin").click()

    h1_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.page-heading"))
    )
    assert h1_element.text == "MY ACCOUNT" or None


#TC02: Kiểm tra hiển thị thông báo chức năng đăng nhập khi bỏ trống email.
def test_case_02(driver):
    driver.find_element(By.ID, "passwd").send_keys("abc123")
    driver.find_element(By.ID, "SubmitLogin").click()
    
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert.alert-danger ol li"))
    )
    assert error_message.text == "An email address required." or None

#TC03: Kiểm tra hiển thị thông báo chức năng đăng nhập khi bỏ trống mật khẩu. 
def test_case_03(driver):
    driver.find_element(By.ID, "email").send_keys("ndtai0912@gmail.com")
    driver.find_element(By.ID, "SubmitLogin").click()
    
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert.alert-danger ol li"))
    )
    assert error_message.text == "Password is required." or None


#TC04: Kiểm tra hiển thị thông báo nhập sai email và mật khẩu. 
def test_case_04(driver):
    driver.find_element(By.ID, "email").send_keys("akjsndjkansd@gmail.com")
    driver.find_element(By.ID, "passwd").send_keys("ádkjasdhnask")
    driver.find_element(By.ID, "SubmitLogin").click()
    
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert.alert-danger ol li"))
    )
    assert error_message.text == "Authentication failed." or None

#TC05: Kiểm tra đăng xuất thành công.
def test_case_05(driver):
    driver.find_element(By.ID, "email").send_keys("ndtai0912@gmail.com")
    driver.find_element(By.ID, "passwd").send_keys("abc123")
    driver.find_element(By.ID, "SubmitLogin").click()

    driver.find_element(By.CLASS_NAME, "logout").click()
    h1_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.page-heading"))
    )
    assert h1_element.text == "AUTHENTICATION" or None




