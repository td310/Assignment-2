#cd cart

#---Batch Execution---
#pytest cart_test.py

#---Individual Execution---
#pytest -k "test_case_01" cart_test.py
#pytest -k "test_case_02" cart_test.py
#pytest -k "test_case_03" cart_test.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time

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

#Kiểm tra thêm vào giỏ hàng thành công.
def test_case_01(driver):
    #chọn vào tên sản phẩm Blouse
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-name"))
    )
    driver.find_element(By.LINK_TEXT, "Blouse").click()
    time.sleep(2)

    #chọn size sản phẩm (selection) 
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "group_1"))
    )
    size_select = driver.find_element(By.ID, "group_1")
    size_select.click() 
    time.sleep(2)

    #click vào size L 
    size_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//option[@value='3']"))
    )
    size_option.click()
    time.sleep(2)

    #add to cart
    driver.find_element(By.NAME, "Submit").click()
    time.sleep(2)

    success_message = WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.TAG_NAME, "h2").text
    )
    assert success_message == "Product successfully added to your shopping cart"

#Kiểm tra cập nhật số lượng sản phẩm trong cart.
def test_case_02(driver):
    #chọn vào tên sản phẩm Blouse
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-name"))
    )
    driver.find_element(By.LINK_TEXT, "Blouse").click()
    time.sleep(2)
     
    #chọn size sản phẩm (selection) 
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "group_1"))
    )
    size_select = driver.find_element(By.ID, "group_1")
    size_select.click() 
    time.sleep(2)

    #click vào size L
    size_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//option[@value='3']"))
    )
    size_option.click()
    time.sleep(2)

    #add to cart
    driver.find_element(By.NAME, "Submit").click()
    time.sleep(2)

    #chọn vào nút checkout để qua trang cart
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='Proceed to checkout']"))
    )
    checkout_button.click()
    time.sleep(2)

    #xác định số lượng sản phẩm ban đầu
    quantity_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.cart_quantity_input"))
    )
    initial_quantity = int(quantity_element.get_attribute("value"))
    assert initial_quantity == 1

    #click để tăng số lượng sản phẩm
    add_quantity_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cart_quantity_up_2_11_0_0"))
    )
    add_quantity_button.click()
    time.sleep(2)

    #kiểm tra
    updated_quantity = int(quantity_element.get_attribute("value"))
    assert updated_quantity == initial_quantity + 1


#Kiểm tra xóa sản phẩm khỏi giỏ hàng.
def test_case_03(driver):
    #chọn vào tên sản phẩm Blouse
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-name"))
    )
    driver.find_element(By.LINK_TEXT, "Blouse").click()
    time.sleep(2)
     
    #chọn size sản phẩm (selection) 
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "group_1"))
    )
    size_select = driver.find_element(By.ID, "group_1")
    size_select.click() 
    time.sleep(2)

    #click vào size L
    size_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//option[@value='3']"))
    )
    size_option.click()
    time.sleep(2)

    #add to cart
    driver.find_element(By.NAME, "Submit").click()
    time.sleep(2)

    #chọn vào nút checkout để qua trang cart
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='Proceed to checkout']"))
    )
    checkout_button.click()
    time.sleep(2)

    #click để xóa sản phẩm
    delete_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "cart_quantity_delete"))
    )
    delete_button.click()
    time.sleep(2)

    empty_cart = driver.find_element(By.CLASS_NAME, "alert-warning")
    assert empty_cart.text == "Your shopping cart is empty." or None

#Thêm nhiều sp vào giỏ hàng
def test_case_04(driver):
    products = ["Blouse", "Printed Summer Dress", "Printed Chiffon Dress"]

    for product in products:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".product-name"))
        )
        
        #click vào tên sản phẩm
        driver.find_element(By.LINK_TEXT, product).click()
        time.sleep(2)

        #chọn size sp
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "group_1"))
        )
        size_select = driver.find_element(By.ID, "group_1")
        size_select.click() 
        time.sleep(2)

        #click vào size L
        size_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//option[@value='3']"))
        )
        size_option.click()
        time.sleep(2)

        #thêm vào giỏ hàng
        driver.find_element(By.NAME, "Submit").click()
        time.sleep(2)

        #chọn continue shopping
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@title='Continue shopping']"))
        )
        driver.find_element(By.XPATH, "//span[@title='Continue shopping']").click()
        time.sleep(2)

        #quay về trang sản phẩm
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@title='Women']"))
        )
        driver.find_element(By.XPATH, "//a[@title='Women']").click()
        time.sleep(2)

    #click vào giỏ hàng
    cart = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='View my shopping cart']"))
    )
    cart.click()

    #tìm tên sp trong giỏ hàng
    cart_product_names = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart_description .product-name"))
    )

    #lấy tên sp
    cart_product_names_text = [name.text for name in cart_product_names]

    #kiểm tra tên sp
    for i, product in enumerate(products):
        assert cart_product_names_text[i] == product
