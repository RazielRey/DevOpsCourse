import unittest
from test_auth import AuthenticationTests
from test_domains import DomainManagementTests
from test_scheduler import SchedulerTests
from conftest import test_logger as logging

def run_all_tests():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    test_cases = [AuthenticationTests, DomainManagementTests, SchedulerTests]
    for test_case in test_cases:
        suite.addTests(loader.loadTestsFromTestCase(test_case))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)

if __name__ == '__main__':
    run_all_tests()