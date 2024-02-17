import time
import unittest

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC

class TestLogin(unittest.TestCase):

    USER_NAME_FIELD = (By.CSS_SELECTOR, "#user-name")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "#password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[type=\"submit\"]")
    PRODUCT_LABEL = (By.CSS_SELECTOR, ".product_label")
    ERROR_MESSAGE = (By.XPATH, "//h3[@data-test=\"error\"]")

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(("https://www.saucedemo.com/v1/index.html"))
        self.driver.maximize_window()
        # For all the searched elements we'll wait maximum 2 sec before trowing the error Element not found
        self.driver.implicitly_wait(2)

    def tearDown(self):
        self.driver.quit()

    # @unittest.skip
    def test_login_standard_user(self):
        user_name_field = self.driver.find_element(*self.USER_NAME_FIELD)
        # * unpacks the USER_NAME_FIELD tuple declared as a constant at the beginning
        # *self.USER_NAME_FIELD unpacks the tuple (By.CSS_SELECTOR, "#user-name") => By.CSS_SELECTOR, "#user-name"
        user_name_field.send_keys("standard_user")

        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        password_field.send_keys("secret_sauce")

        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        login_button.click()

        product_label = self.driver.find_elements(*self.PRODUCT_LABEL)
        self.assertTrue(len(product_label) >= 1, "Element not found. Login not working correctly")

    def test_login_incorrect_password(self):
        # Wait maximum 4 sec for user_name_field
        user_name_field = WebDriverWait(self.driver, 4).until(
            EC.presence_of_element_located(self.USER_NAME_FIELD))
        user_name_field.send_keys("standard_user")

        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        password_field.send_keys("wrong_password")

        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        login_button.click()

        error_message = self.driver.find_element(*self.ERROR_MESSAGE)
        self.assertEqual(error_message.text,
                         "Epic sadface: Username and password do not match any user in this service",
                         "Error message not displayed")
