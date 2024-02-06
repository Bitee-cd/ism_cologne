from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

product_url ="https://www.ism-cologne.com/exhibitor"
URL = product_url
base_url = "https://www.ism-cologne.com"

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(URL)
driver.maximize_window()

total_data=[]
filtered_urls = []
def reject_cookies():
    try:
        reject_button = WebDriverWait(driver,5).until(
            EC.presence_of_all_elements_located((By.ID,"onetrust-reject-all-handler"))
        )
        if len(reject_button) > 0:
            reject_button[0].click()
        else:
            return
    except NoSuchElementException:
        print("an element was not found")


def get_available_items():

    while True:
        # Get list of items on the current page
        items_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
        )
        list_of_items = WebDriverWait(items_container, 5).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        for item in list_of_items:
            url = item.get_attribute("href")
            if url is not None and url.startswith("https://www.ism-cologne.com/exhibitor/"):
                filtered_urls.append(url)

        # Check if there is a "Next" button
        pagination_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pagination-footer"))
        )
        next_buttons = pagination_container.find_elements(By.CLASS_NAME, "slick-next")
        if len(next_buttons) > 0:
            # Click the "Next" button
            next_buttons[0].click()
            time.sleep(10)
        else:
            # No more "Next" button, break out of the loop
            break

    # Write the URLs to a file
    with open("urls.txt", "w") as file:
        for url in filtered_urls:
            file.write(url + "\n")


reject_cookies()
get_available_items()



