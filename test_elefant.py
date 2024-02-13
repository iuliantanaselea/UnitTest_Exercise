from unittest import TestCase

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC


class MyTestCase(TestCase):
    COOKIE_BUTTON = (By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    ELEFANT_LOGO = (By.XPATH, "//img[@alt=\"Logo\"]")
    SEARCH_BAR = (By.XPATH, "//form//input [@name=\"SearchTerm\"]")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "form > button[name = \"search\"]")
    DISPLAY_PRODUCTS = (By.CSS_SELECTOR, ".product-list >.product-list-item")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "[class=\"current-price \"]")

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get("https://www.elefant.ro/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(3)

        # Try to identify and accept cookies, if it doesn't exist, move on with this try except
        try:
            self.driver.find_element(*self.COOKIE_BUTTON).click()
        except NoSuchElementException:
            pass

    def tearDown(self):
        self.driver.quit()

    def test_verificare_pagina_elefant(self):
        elefant_logo = self.driver.find_element(*self.ELEFANT_LOGO)
        self.assertTrue(elefant_logo.is_displayed())

    def test_search_bar(self):
        search_bar_element = self.driver.find_element(*self.SEARCH_BAR)
        search_bar_element.send_keys("iphone 14")

        search_button_element = self.driver.find_element(*self.SEARCH_BUTTON)
        search_button_element.click()

        display_products_elements = self.driver.find_elements(*self.DISPLAY_PRODUCTS)
        self.assertTrue(len(display_products_elements) >= 5, "Eroare, nu a returnat 5 elemente")

    def test_title(self):
        self.assertEqual("elefant.ro - mallul online al familiei tale! • Branduri de top, "
                         "preturi excelente • Peste 500.000 de produse pentru tine!", self.driver.title)

    def test_pick_lowest_price(self):
        search_bar_element = self.driver.find_element(*self.SEARCH_BAR)
        search_bar_element.send_keys("iphone 14")

        search_button_element = self.driver.find_element(*self.SEARCH_BUTTON)
        search_button_element.click()

        # self.driver.get("https://www.elefant.ro/search?SearchTerm=iphone+14&StockAvailability=true")
        price_products_element= self.driver.find_elements(*self.PRODUCT_PRICES)

        #Option 1

        price_list = []
        for element in price_products_element:
            for i in element.text.split(" "):
                i= i.replace(".", "")
                i= i.replace(",", ".")
                # print(i)
                if i.isdigit():
                    price_list.append(float(i))
        # print(price_list)
        price_list.sort()
        print("-"*30)
        print(price_list[0])
        self.assertEqual(57.0, price_list[0]) # There is a chance that it updates due to the changed prices on the site


        #Option 2
        """
        l = price_products_element
        print(l)
        price_list= []
        list_raw = []

        for pret_i in price_products_element:
            pret_raw = pret_i.get_attribute("data-price")
            list_raw.append(pret_raw)

            pret = pret_raw.replace(".", "")
            pret_i = int(pret)
            pret_f = pret_i / 100
            price_list.append(pret_f)
        print(list_raw)
        print(min(price_list))
        print(min(price_list))
        """

