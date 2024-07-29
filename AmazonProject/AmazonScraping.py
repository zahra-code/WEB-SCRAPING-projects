import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

service=Service(executable_path="../chromedriver.exe")
driver=webdriver.Chrome(service=service)
try:
    driver.implicitly_wait(5)
    file =1
    query="Keyboards"
    for i in range(1,20):
        driver.get(F"https://www.amazon.in/s?k={query}&page={i}&crid=37E2E89ICO5GG&qid=1719652912&sprefix={query}%2Caps%2C289&ref=sr_pg_{i}")
        print("STARTING collecting data...")
        WebDriverWait(driver,5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,'div[data-component-type="s-search-result"]')
            )
        )

        elements=driver.find_elements(By.CSS_SELECTOR,'div[data-component-type="s-search-result"]')
        print(f"\tTotal {len(elements)} found at page {i}")
        for element in elements:
            html_content=element.get_attribute("outerHTML")
            with open(f"data/{query}_file{file}.html","w",encoding='utf-8') as f:
                f.write(html_content)
        file+=1
        time.sleep(2)
        print("\n")
    print(f"{file} HTML files collected for {query.capitalize()}")
    driver.quit()
except Exception as e:
    print(f"ERRROR: {e}")