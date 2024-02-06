from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException,TimeoutException


class SinglePageDetails:
    def __init__(self,url):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(url)
        self.driver.maximize_window()
        self.page_data = []

    def reject_cookies(self):
        try:
            reject_button = WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.ID,"onetrust-reject-all-handler"))
            )
            reject_button.click()
        except NoSuchElementException:
            print("an element was not found")


    def fetch_product_groups(self):
        try:
            section= WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.CLASS_NAME,"asdb54-aussteller-detailseite-content"))
            )
            title_container = WebDriverWait(section,5).until(
                EC.presence_of_element_located((By.CLASS_NAME,"headline-title"))
            )
            title = title_container.find_element(By.TAG_NAME,"span").text

            product_groups_container = WebDriverWait(section,5).until(
                EC.presence_of_element_located((By.CLASS_NAME,"asdb-cap-products-list"))
            )
            product_groups_list = product_groups_container.find_element(By.CLASS_NAME,"level-1")
            product_groups = product_groups_list.find_elements(By.CLASS_NAME,"hassub")
            product_groups_array=[]
            for product_group in product_groups:
                product_group_name = product_group.find_element(By.TAG_NAME,"div").get_attribute("innerHTML")
                products_list = product_group.find_elements(By.TAG_NAME,"a")
                products =[]
                for product in products_list:
                    product_name = product.get_attribute("innerHTML")
                    products.append(product_name)
                product_groups_array.append({"product_group_name":product_group_name,"products":products})
            self.page_data.append({"title":title,"product_groups":product_groups_array})
        except NoSuchElementException:
            print("an element was not found")
            return
        except TimeoutException:
            print("Timed out waiting for element")
            return

    def fetch_brands(self):
        try:
            brands_section= WebDriverWait(self.driver,5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,"asdb54-cap-products-list"))
            )
            brands=[]
            if len(brands_section) > 0:
                brands_list= WebDriverWait(brands_section[0], 5).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "titel"))
                )
                for brand in brands_list:

                    brand_name = brand.get_attribute("innerHTML")
                    brands.append(brand_name.encode().decode('utf-8').strip())
                self.page_data.append({"brands":brands})
            else:
                print("brands element was not found")
                return
        except NoSuchElementException:
            print("brands element was not found")
            return
        except TimeoutException:
            print("Timed out waiting for element")
            return
    def other_details(self):
        try:
            other_section= WebDriverWait(self.driver,5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,"austellerdetail_gruppe"))
            )
            sections= WebDriverWait(other_section[2], 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "db-acc"))
            )
            for section in sections:

                section_title = section.find_element(By.CLASS_NAME,"db-acctitle").text
                section_items_container = section.find_elements(By.CLASS_NAME,"asdb54-singleInfo-gruppierung")
                section_items=[]
                for item in section_items_container:
                    section_items.append(item.get_attribute("innerHTML"))

                self.page_data.append({section_title:section_items})
        except NoSuchElementException:
            print("brands element was not found")
            return
        except TimeoutException:
            print("Timed out waiting for element")
            return




    def close_page(self):
        self.driver.quit()

    def run_scraper(self):
        self.reject_cookies()
        self.fetch_product_groups()
        self.fetch_brands()
        self.other_details()
        self.close_page()
        return self.page_data

