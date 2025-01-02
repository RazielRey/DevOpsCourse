from test_base import BaseTest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from conftest import test_logger as logging

class DomainManagementTests(BaseTest):

    def setUp(self):
        """Setup for domain tests - login to the application"""
        super().setUp()
        logging.info("Starting domain tests setup")
        self.login()
        logging.info("Login successful")

    def login(self):
        """Helper method to login before tests"""
        logging.info("Performing login")
        self.driver.get(self.base_url)
        
        username_field = self.wait_for_element(By.ID, "username")
        password_field = self.wait_for_element(By.ID, "password")
        
        username_field.send_keys("testuser")
        password_field.send_keys("Test123!")
        
        login_button = self.wait_for_element(By.ID, "login")
        login_button.click()
        
        # Wait for dashboard to load
        try:
            self.wait_for_element(By.CLASS_NAME, "dashboard-title", timeout=15)
            logging.info("Login successful")
        except TimeoutException:
            logging.error("Failed to login - dashboard not loaded")
            self.fail("Could not login before domain test")

    def test_add_domain(self):
        """Test adding a domain"""
        logging.info("Starting test to add a domain")
        
        # Find and fill the domain input
        try:
            domain_field = self.wait_for_element(By.ID, "domainInput")
            test_domain = "example.com"
            domain_field.send_keys(test_domain)
            logging.info(f"Domain entered: {test_domain}")

            # Click add button (using correct class name)
            add_button = self.wait_for_element(By.CLASS_NAME, "add-button")
            add_button.click()
            logging.info("Add button clicked")

            # Wait for AJAX request to complete
            time.sleep(2)

            # Verify domain in table
            table = self.wait_for_element(By.CLASS_NAME, "domains-table")
            domain_cells = table.find_elements(By.CLASS_NAME, "domain-name")
            
            domain_found = any(cell.text == test_domain for cell in domain_cells)
            if domain_found:
                logging.info("Domain successfully added to table")
                self.assertTrue(domain_found)
            else:
                logging.error("Added domain not found in table")
                self.fail("Domain not found in table after adding")

        except TimeoutException as e:
            logging.error(f"Failed to add domain: {e}")
            self.fail("Could not complete domain addition test")


    def test_delete_domain(self):
        """Test deleting a domain"""
        logging.info("Starting delete domain test")
        
        try:
            # Add a domain to delete
            test_domain = "delete-test.com"
            domain_field = self.wait_for_element(By.ID, "domainInput")
            domain_field.send_keys(test_domain)
            
            add_button = self.wait_for_element(By.CLASS_NAME, "add-button")
            add_button.click()
            logging.info(f"Added test domain: {test_domain}")
            
            time.sleep(2)  # Wait for domain to be added
            
            # Click delete button
            delete_button = self.wait_for_element(By.CLASS_NAME, "delete-button")
            delete_button.click()
            logging.info("Delete button clicked")

            # Handle confirmation alert
            self.handle_alerts()

            # Wait for table to update
            logging.info("Waiting for table update after deletion")
            WebDriverWait(self.driver, 10).until(
                lambda driver: all(cell.text != test_domain for cell in driver.find_elements(By.CLASS_NAME, "domain-name")),
                "Domain was not removed from the table"
            )
            logging.info("Table updated successfully")

            # Verify that the domain was deleted
            logging.info("Verifying domain deletion")
            table = self.wait_for_element(By.CLASS_NAME, "domains-table")
            domain_cells = table.find_elements(By.CLASS_NAME, "domain-name")
            
            domain_found = any(cell.text == test_domain for cell in domain_cells)
            if domain_found:
                logging.error("Domain still exists after deletion")
                self.fail("Domain still in table after deletion") 
            else:
                logging.info("Domain successfully deleted")
                self.assertTrue(True)
                
        except TimeoutException as e:
            logging.error(f"Failed to delete domain: {e}")
            self.fail("Could not complete domain deletion test")


    def test_refresh_domains(self):
        """Test refreshing domain statuses"""
        logging.info("Starting refresh domains test")
        
        try:
            # First add a test domain
            test_domain = "refresh-test.com"
            domain_field = self.wait_for_element(By.ID, "domainInput")
            domain_field.send_keys(test_domain)
            add_button = self.wait_for_element(By.CLASS_NAME, "add-button")
            add_button.click()
            logging.info(f"Added test domain: {test_domain}")
            
            time.sleep(2)  # Wait for domain to be added
            
            # Store initial status
            initial_status = None
            status_badge = self.wait_for_element(By.CLASS_NAME, "status-badge")
            initial_status = status_badge.text
            logging.info(f"Initial status: {initial_status}")

            # Click refresh
            refresh_button = self.wait_for_element(By.CLASS_NAME, "refresh-button")
            refresh_button.click()
            logging.info("Clicked refresh button")

            # Wait for spinner to appear and disappear
            spinner = self.wait_for_element(By.ID, "spinner")
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.ID, "spinner"))
            )
            logging.info("Refresh completed (spinner gone)")

            # Verify status was updated
            time.sleep(2)  # Give time for table to update
            new_status_badge = self.wait_for_element(By.CLASS_NAME, "status-badge")
            new_status = new_status_badge.text
            logging.info(f"New status: {new_status}")

            # Verify refresh occurred
            if new_status in ['OK', 'FAILED']:
                logging.info("Domain status refreshed successfully")
                self.assertTrue(True)
            else:
                logging.error("Invalid status after refresh")
                self.fail("Invalid status after refresh")
                
        except TimeoutException as e:
            logging.error(f"Failed to refresh domains: {e}")
            self.fail("Could not complete domain refresh test")
                