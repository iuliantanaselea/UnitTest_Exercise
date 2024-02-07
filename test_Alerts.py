import time
from unittest import TestCase
import unittest

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC


class TestAlerts(TestCase):
    # Define a constant called TEXT
    TEXT = "added text"
    JS_ALERT_BUTTON = (By.XPATH, "//li//button[contains(text(), \"Click for JS Alert\")]")
    JS_CONFIRM_BUTTON = (By.XPATH, "//li//button[contains(text(), \"Click for JS Confirm\")]")
    JS_PROMPT_BUTTON = (By.XPATH, "//li//button[contains(text(), \"Click for JS Prompt\")]")
    RESULT_MESSAGE_PARAGRAPH = (By.CSS_SELECTOR, "#result")

    def setUp(self):
        #Set the running in background
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")

        #Execute the regular code, but with "options=chrome_options" argument added in the line below
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        self.driver.maximize_window()
        # For all the searched elements we'll wait maximum 3 sec before trowing the error Element not found
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.quit()

    def test_alert(self):
        js_alert_button_element = self.driver.find_element(*self.JS_ALERT_BUTTON)
        js_alert_button_element.click()
        # time.sleep(3)
        js_alert = self.driver.switch_to.alert
        js_alert.accept()
        # time.sleep(2)
        js_alert_result_message_paragraph = self.driver.find_element(*self.RESULT_MESSAGE_PARAGRAPH)
        self.assertEqual("You successfully clicked an alert", js_alert_result_message_paragraph.text)

    def test_confirm_alert(self):
        js_confirm_button_element = self.driver.find_element(*self.JS_CONFIRM_BUTTON)
        js_confirm_button_element.click()
        js_confirm_alert = self.driver.switch_to.alert
        js_confirm_alert.accept()
        js_alert_result_message_paragraph = self.driver.find_element(*self.RESULT_MESSAGE_PARAGRAPH)
        self.assertEqual("You clicked: Ok", js_alert_result_message_paragraph.text)

    def test_dismiss_alert(self):
        js_confirm_button_element = self.driver.find_element(*self.JS_CONFIRM_BUTTON)
        js_confirm_button_element.click()
        js_confirm_alert = self.driver.switch_to.alert
        js_confirm_alert.dismiss()
        js_alert_result_message_paragraph = self.driver.find_element(*self.RESULT_MESSAGE_PARAGRAPH)
        self.assertEqual("You clicked: Cancel", js_alert_result_message_paragraph.text)

    def test_prompt_ok(self):
        js_prompt_button_element = self.driver.find_element(*self.JS_PROMPT_BUTTON)
        js_prompt_button_element.click()
        js_prompt_alert = self.driver.switch_to.alert
        js_prompt_alert.accept()
        js_alert_result_message_paragraph = self.driver.find_element(*self.RESULT_MESSAGE_PARAGRAPH)
        self.assertEqual("You entered:", js_alert_result_message_paragraph.text)

    def test_prompt_cancel(self):
        js_prompt_button_element = self.driver.find_element(*self.JS_PROMPT_BUTTON)
        js_prompt_button_element.click()
        js_prompt_alert = self.driver.switch_to.alert
        js_prompt_alert.dismiss()
        js_alert_result_message_paragraph = self.driver.find_element(*self.RESULT_MESSAGE_PARAGRAPH)
        self.assertEqual("You entered: null", js_alert_result_message_paragraph.text)

    def test_prompt_accept_text(self):
        js_prompt_button_element = self.driver.find_element(*self.JS_PROMPT_BUTTON)
        js_prompt_button_element.click()

        # Action 1 alert --> send the text in the field
        js_prompt_alert = self.driver.switch_to.alert
        js_prompt_alert.send_keys(self.TEXT)

        # Action 2 alert --> Click "Ok" after adding the text
        js_prompt_alert.accept()

        js_alert_result_message_paragraph = self.driver.find_element(*self.RESULT_MESSAGE_PARAGRAPH)
        self.assertEqual(f"You entered: {self.TEXT}", js_alert_result_message_paragraph.text)

    def test_prompt_cancel_text(self):
        js_prompt_button_element = self.driver.find_element(*self.JS_PROMPT_BUTTON)
        js_prompt_button_element.click()

        # Action 1 alert --> send the text in the field
        js_prompt_alert = self.driver.switch_to.alert
        js_prompt_alert.send_keys(self.TEXT)

        # Action 2 alert --> Click Cancel after adding the text
        js_prompt_alert.dismiss()

        js_alert_result_message_paragraph = self.driver.find_element(*self.RESULT_MESSAGE_PARAGRAPH)
        self.assertEqual("You entered: null", js_alert_result_message_paragraph.text)
