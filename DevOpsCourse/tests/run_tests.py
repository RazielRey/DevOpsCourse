import unittest
from test_auth import AuthenticationTests
from test_domains import DomainManagementTests
from test_scheduler import SchedulerTests

def create_test_suite():
    """Create a test suite containing all tests"""
    suite = unittest.TestSuite()
    
    # Add all test classes
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(AuthenticationTests))
    suite.addTests(loader.loadTestsFromTestCase(DomainManagementTests))
    suite.addTests(loader.loadTestsFromTestCase(SchedulerTests))
    
    return suite

if __name__ == '__main__':
    # Run the test suite
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)