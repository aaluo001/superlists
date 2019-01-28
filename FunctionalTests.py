#!python
# coding: gbk
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
        
        # 页面的标题和开头都包含 "To-Do" 这个词
        self.assertIn('待办事项', self.vBrowser.title)
        self.assertIn('待办事项', self.vBrowser.find_element_by_tag_name('h1').text)
        
        # 页面有一个待办事项文本输入框
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        self.assertEqual(vInputBox.get_attribute('placeholder'), '试试输入一个待办事项吧')
        
        
        # 输入第一个待办事项
        vInputBox.send_keys('买一些孔雀羽毛')
        vInputBox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # 查看刚刚输入的待办事项
        vTable = self.vBrowser.find_element_by_id('id_list_table')
        vRows = vTable.find_elements_by_tag_name('tr')
        self.assertIn('1: 买一些孔雀羽毛', [ vRow.text for vRow in vRows ])
        
        
        # 输入第二个待办事项
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        vInputBox.send_keys('用孔雀羽毛做假蝇')
        vInputBox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # 再次查看刚刚输入的待办事项
        vTable = self.vBrowser.find_element_by_id('id_list_table')
        vRows = vTable.find_elements_by_tag_name('tr')
        self.assertIn('1: 买一些孔雀羽毛',   [ vRow.text for vRow in vRows ])
        self.assertIn('2: 用孔雀羽毛做假蝇', [ vRow.text for vRow in vRows ])


        self.fail('Finish The Test!')



if (__name__ == '__main__'):
    #unittest.main(warnings='ignore')
    unittest.main()
