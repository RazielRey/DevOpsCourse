import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
import logging 
import requests

class BaseTest(unittest.TestCase):
    def setUp(self):
        # Set up the browser
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8080"
        
        # Create a test user
        self.create_test_user()

    def tearDown(self):
        # Close the browser
        if self.driver:
            self.driver.quit()

    def wait_for_element(self, by, value, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except UnexpectedAlertPresentException:
            logging.warning("Unexpected alert present. Handling it.")
            alert = self.driver.switch_to.alert
            logging.info(f"Alert text: {alert.text}")
            alert.accept()
            logging.info("Alert dismissed.")
            # Re-raise the exception if needed or retry finding the element
            raise
    def handle_alerts(self):
        """Handle all pending alerts"""
        try:
            while True:
                logging.info("Checking for alerts...")
                WebDriverWait(self.driver, 3).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                logging.info(f"Alert found with text: {alert.text}")
                alert.accept()
                logging.info("Alert dismissed.")
        except TimeoutException:
            logging.info("No more alerts present.")



    def create_test_user(self): 
        """Create a test user if it does not exist"""
        user_data = {
            "username": "testuser",
            "password": "Test123!"
        }
        try:
            response = requests.post(f"{self.base_url}/NewUser", data=user_data)
            if response.status_code == 200:
                print("Test user created successfully")
            elif "already exists" in response.text:
                print("Test user already exists")
            else:
                print("Failed to create test user")
        except Exception as e:
            print(f"Error creating test user: {e}")
