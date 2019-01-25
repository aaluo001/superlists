#!python
# FunctionalTests.py

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
  
    def setUp(self):
        self.vBrowser = webdriver.Firefox()
  
    def tearDown(self):
        self.vBrowser.quit()


    def test_CanStartAListAndRetrieveItLater(self):
        self.vBrowser.get('http://localhost:8000')
        
        self.assertIn('To-Do', self.vBrowser.title)
        self.assertIn('To-Do', self.vBrowser.find_element_by_tag_name('h1').text)
        
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        self.assertEqual(vInputBox.get_attribute('placeholder'), 'Enter a to-do item')
        
        vInputBox.send_keys('Buy peacock feathers')
        vInputBox.send_keys(Keys.ENTER)
        time.sleep(2)
        
        vTable = self.vBrowser.find_element_by_id('id_list_table')
        vRows = vTable.find_elements_by_tag_name('tr')
        self.assertTrue( \
            any(vRow.text == '1: Buy peacock feathers' for vRow in vRows), \
            'New to-do item did not appear in table' \
        )
        
        
        self.fail('Finish The Test!')



if (__name__ == '__main__'):
    #unittest.main(warnings='ignore')
    unittest.main()
