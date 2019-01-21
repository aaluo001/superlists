#!python
# FunctionalTests.py

import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
  
  def setUp(self):
    self.vBrowser = webdriver.Firefox()
  
  def tearDown(self):
    self.vBrowser.quit()


  def test_CanStartAListAndRetrieveItLater(self):
    self.vBrowser.get('http://localhost:8000')

    self.assertIn('To-Do', self.vBrowser.title)
    self.fail('Finish the test!')



if (__name__ == '__main__'):
  #unittest.main(warnings='ignore')
  unittest.main()
