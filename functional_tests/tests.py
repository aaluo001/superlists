#!python
# coding: gbk
# tests.py

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):
  
    def setUp(self):
        self.vBrowser = webdriver.Firefox()
  
    def tearDown(self):
        self.vBrowser.quit()

    def checkForRowInListTable(self, vRowText):
        vTable = self.vBrowser.find_element_by_id('id_list_table')
        vRows = vTable.find_elements_by_tag_name('tr')
        self.assertIn(vRowText, [ vRow.text for vRow in vRows ])


    def test_CanStartAListAndRetrieveItLater(self):
        # 访问应用首页
        self.vBrowser.get(self.live_server_url)
        
        # 页面的标题和开头都包含 "To-Do" 这个词
        self.assertIn('待办事项', self.vBrowser.title)
        self.assertIn('待办事项', self.vBrowser.find_element_by_tag_name('h1').text)
        
        # 页面有一个待办事项文本输入框
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        self.assertEqual(vInputBox.get_attribute('placeholder'), '试试输入一个待办事项吧')
        
        
        # 输入第一个待办事项
        vInputBox.send_keys('买一些孔雀羽毛')
        vInputBox.send_keys(Keys.ENTER)
        time.sleep(3)
        
        # 查看刚刚输入的待办事项
        self.checkForRowInListTable('1: 买一些孔雀羽毛')
        

        # 输入第二个待办事项
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        vInputBox.send_keys('用孔雀羽毛做假蝇')
        vInputBox.send_keys(Keys.ENTER)
        time.sleep(3)
        
        # 再次查看刚刚输入的待办事项
        self.checkForRowInListTable('1: 买一些孔雀羽毛')
        self.checkForRowInListTable('2: 用孔雀羽毛做假蝇')


        self.fail('Finish The Test!')

