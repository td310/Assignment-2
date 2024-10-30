#cd reponsive
#---Batch Execution
#pytest reponsive_test.py
#---Individual Execution---
#pytest -k "test_responsive_design" reponsive_test.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import pytest
import time

@pytest.fixture(params=["chrome", "edge"])
def driver(request):
    if request.param == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--window-size=1920,1080")  
        driver = webdriver.Chrome(options=chrome_options)
    elif request.param == "edge":
        edge_options = EdgeOptions()
        edge_options.add_argument("--headless")  
        edge_options.add_argument("--window-size=1920,1080")  
        driver = webdriver.Edge(options=edge_options)

    driver.get("http://www.automationpractice.pl/index.php")
    yield driver
    driver.quit()

#TC: Kiểm tra reponsive trên 2 trình duyệt Edge và Chrome
def test_responsive_design(driver):
    screen_sizes = [(1920, 1080), (1366, 768), (768, 1024), (375, 667)]

    for width, height in screen_sizes:
        driver.set_window_size(width, height)
        time.sleep(2)

        logo = driver.find_element(By.CLASS_NAME, "logo")
        assert logo.is_displayed(), f"Logo không hiển thị ở kích thước {width}x{height}"


