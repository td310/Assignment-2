import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

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
def test_check_links(driver):
    
    links = driver.find_elements(By.TAG_NAME, "a")
    
    for link in links:
        url = link.get_attribute("href")  
        if url:  
            response = requests.head(url)  
            status_code = response.status_code
            if status_code >= 400:
                print(f"Hỏng: {url} (Status: {status_code})")
            else:
                print(f"Hợp lệ: {url} (Status: {status_code})")

