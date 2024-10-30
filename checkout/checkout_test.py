#cd cart

#---Batch Execution---
#pytest -v

#---Individual Execution---
#pytest -k "test_case_01" checkout.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time
import random

@pytest.fixture(params=["chrome", "edge"])
def driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "edge":
        driver = webdriver.Edge()
    driver.get("http://www.automationpractice.pl/index.php?id_category=3&controller=category")
    driver.maximize_window()
    yield driver
    driver.quit()

#Kiểm tra checkout bằng "pay by bank wire" và thêm address mới
def test_case_01(driver):
    #1, chọn vào tên sản phẩm Blouse
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-name"))
    )
    driver.find_element(By.LINK_TEXT, "Blouse").click()

    #2.1, chọn size sản phẩm (selection)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "group_1"))
    )
    size_select = driver.find_element(By.ID, "group_1")
    size_select.click()
    time.sleep(2)

    #2.2, click vào size L
    size_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//option[@value='3']"))
    )
    size_option.click()
    time.sleep(2)

    #3, add to cart
    driver.find_element(By.NAME, "Submit").click()
    time.sleep(2)

    #4, click vào nút checkout để qua trang cart
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='Proceed to checkout']"))
    )
    checkout_button.click()

    #5, click vào checkout -> chuyển hướng qua trang login
    final_checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[@title='Proceed to checkout' and contains(@href, 'controller=order&step=1')]")
        )
    )
    final_checkout_button.click()

    #6,Login
    driver.find_element(By.ID, "email").send_keys("ndtai0912@gmail.com")
    driver.find_element(By.ID, "passwd").send_keys("abc123")
    time.sleep(2)
    driver.find_element(By.ID, "SubmitLogin").click()

    #7, click để tạo 1 address mới
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Add a new address"))
    )
    link.click()
    time.sleep(2)
    #8, nhập các trường trong form
    driver.find_element(By.ID, "firstname").send_keys("John")
    driver.find_element(By.ID, "lastname").send_keys("Doe")
    driver.find_element(By.ID, "address1").send_keys("123 abc street")
    driver.find_element(By.ID, "city").send_keys("Los Angeles")

    #9.1, click vào selection State
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "id_state"))
    )
    size_select = driver.find_element(By.ID, "id_state")
    size_select.click()
    time.sleep(2)

    #9.2, chọn value = 3
    size_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//option[@value='3']"))
    )
    size_option.click()

    driver.find_element(By.ID, "postcode").send_keys("90001")
    driver.find_element(By.ID, "phone").send_keys("1234567890")

    driver.find_element(By.ID, "alias").clear()

    #9.3, tạo địa chỉ ngẫu nhiên
    random_number = random.randint(1, 100)
    driver.find_element(By.ID, "alias").send_keys(f"My Home Address{random_number}")

    #10, lưu address mới
    driver.find_element(By.ID, "submitAddress").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "id_address_delivery"))
    )

    #11.1, chọn vào selection
    home_address_select = driver.find_element(By.ID, "id_address_delivery")
    home_address_select.click()
    time.sleep(2)

    #11.2, click vào address mới
    options = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//select[@id='id_address_delivery']/option"))
    )
    for option in options:
        if option.text == f"My Home Address{random_number}":
            option.click()
            break
    time.sleep(2)

    #12, tiếp tục chọn Proceed to Checkout
    checkout_address = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "processAddress"))
    )
    checkout_address.click()
    time.sleep(2)

    #13, chọn vào checkbox
    checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cgv"))
    )
    if not checkbox.is_selected():
        checkbox.click()

    #14, tiếp tục chọn Proceed to Checkout
    checkout_carrier = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "processCarrier"))
    )
    checkout_carrier.click()

    #15, chọn cách order (Pay by bank wire)
    bank_wire_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.bankwire"))
    )
    bank_wire_link.click()

    #16, confirm order
    confirm_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.btn.btn-default.button-medium"))
    )
    confirm_order_button.click()
    time.sleep(2)

    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "p.alert.alert-success"))
    )
    #kiểm tra check out thành công.
    assert success_message.text == "Your order on My Shop is complete." or None

#Kiểm tra checkout bằng "pay by check"
def test_case_02(driver):
    #1, chọn vào tên sản phẩm Blouse
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-name"))
    )
    driver.find_element(By.LINK_TEXT, "Blouse").click()

    #2.1, chọn size sản phẩm (selection)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "group_1"))
    )
    size_select = driver.find_element(By.ID, "group_1")
    size_select.click()
    time.sleep(2)

    #2.2, click vào size L
    size_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//option[@value='3']"))
    )
    size_option.click()
    time.sleep(2)

    #3, add to cart
    driver.find_element(By.NAME, "Submit").click()
    time.sleep(2)

    #4, click vào nút checkout để qua trang cart
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='Proceed to checkout']"))
    )
    checkout_button.click()

    #5, click vào checkout -> chuyển hướng qua trang login
    final_checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[@title='Proceed to checkout' and contains(@href, 'controller=order&step=1')]")
        )
    )
    final_checkout_button.click()

    #6, Login
    driver.find_element(By.ID, "email").send_keys("ndtai0912@gmail.com")
    driver.find_element(By.ID, "passwd").send_keys("abc123")
    time.sleep(2)
    driver.find_element(By.ID, "SubmitLogin").click()

    #7, tiếp tục chọn Proceed to Checkout
    checkout_address = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "processAddress"))
    )
    checkout_address.click()
    time.sleep(2)

    #8, chọn vào checkbox
    checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cgv"))
    )
    if not checkbox.is_selected():
        checkbox.click()

    #9, tiếp tục chọn Proceed to Checkout
    checkout_carrier = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "processCarrier"))
    )
    checkout_carrier.click()

    #10, chọn cách order (Pay by bank wire)
    check_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.cheque"))
    )
    check_link.click()

    #11, Confirm Order
    confirm_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.btn.btn-default.button-medium"))
    )
    confirm_order_button.click()
    time.sleep(2)

    #12, kiểm tra check out thành công.
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "p.alert.alert-success"))
    )

    assert success_message.text == "Your order on My Shop is complete." or None

