import unittest

import HtmlTestRunner

from test_elefant import MyTestCase
from testKeys import TestCheckBox
from test_Alerts import TestAlerts


class TestSuite(unittest.TestCase):
    def test_suite(self):
        test_suite =unittest.TestSuite()
        test_suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(MyTestCase),
            unittest.defaultTestLoader.loadTestsFromTestCase(TestCheckBox),
            unittest.defaultTestLoader.loadTestsFromTestCase(TestAlerts)
        ])
        runner = HtmlTestRunner.HTMLTestRunner(combine_reports=True,report_title="TestReport",report_name="FirstReport")
        runner.run(test_suite)