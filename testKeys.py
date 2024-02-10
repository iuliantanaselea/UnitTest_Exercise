import time
import unittest

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import selenium.webdriver.support.expected_conditions as EC


class TestCheckBox(unittest.TestCase):
    FULL_NAME_FIELD = (By.CSS_SELECTOR, "#userName")
    EMAIL_FIELD = (By.CSS_SELECTOR, "[placeholder=\"name@example.com\"]")
    CURRENT_ADDRESS_TEXTAREA = (By.XPATH, "//textarea[@id=\"currentAddress\"]")
    PERMANENT_ADDRESS_TEXTAREA = (By.XPATH, "//textarea[@id=\"permanentAddress\"]")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),\"Submit\")]")

    NAME_RESULT = (By.CSS_SELECTOR, "#name")
    EMAIL_RESULT = (By.CSS_SELECTOR, "#email")
    CURRENT_ADDRESS_RESULT = (By.CSS_SELECTOR, "p#currentAddress")
    PERMANENT_ADDRESS_RESULT = (By.CSS_SELECTOR, "p#permanentAddress")

    def setUp(self):
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self.driver.get("https://demoqa.com/text-box")
        self.driver.maximize_window()
        # For all the searched elements we'll wait maximum 3 sec before trowing the error Element not found
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.quit()

    def test_text_box(self):
        full_name_field_element = self.driver.find_element(*self.FULL_NAME_FIELD)
        full_name_field_element.send_keys("John")
        full_name_field_element.send_keys(Keys.BACKSPACE)

        # In the case below, press TAB key and add on the next field (email field) the value "mail@email.com"
        # full_name_field_element.send_keys(Keys.TAB, "mail@email.com")

        email_field_element = self.driver.find_element(*self.EMAIL_FIELD)
        # email_field_element.send_keys("mail@email.com")
        # email_field_element.send_keys("mail", Keys.SHIFT +"2",Keys.SHIFT, "email.com")
        email_field_element.send_keys("mail", Keys.SHIFT + "2")
        email_field_element.send_keys("email.com")

        current_address_element = self.driver.find_element(*self.CURRENT_ADDRESS_TEXTAREA)
        current_address_element.send_keys("Suceada")
        current_address_element.send_keys(Keys.ARROW_LEFT, Keys.BACKSPACE, "v")

        permanent_address_element = self.driver.find_element(*self.PERMANENT_ADDRESS_TEXTAREA)
        permanent_address_element.send_keys("Permanent address")
        permanent_address_element.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)

        submit_button_element = self.driver.find_element(*self.SUBMIT_BUTTON)
        submit_button_element.click()

        name_result_element = self.driver.find_elements(*self.NAME_RESULT)
        email_result_element = self.driver.find_elements(*self.EMAIL_RESULT)
        current_address_result_element = self.driver.find_elements(*self.CURRENT_ADDRESS_RESULT)
        permanent_address_result_element = self.driver.find_elements(*self.PERMANENT_ADDRESS_RESULT)

        self.assertEqual("Name:Joh", name_result_element[0].text)
        self.assertEqual("Email:mail@email.com", email_result_element[0].text)
        self.assertEqual("Current Address :Suceava", current_address_result_element[0].text)
        self.assertTrue(len(permanent_address_result_element) == 0)
        time.sleep(4)
