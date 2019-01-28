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
        
        # ҳ��ı���Ϳ�ͷ������ "To-Do" �����
        self.assertIn('��������', self.vBrowser.title)
        self.assertIn('��������', self.vBrowser.find_element_by_tag_name('h1').text)
        
        # ҳ����һ�����������ı������
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        self.assertEqual(vInputBox.get_attribute('placeholder'), '��������һ�����������')
        
        
        # �����һ����������
        vInputBox.send_keys('��һЩ��ȸ��ë')
        vInputBox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # �鿴�ո�����Ĵ�������
        vTable = self.vBrowser.find_element_by_id('id_list_table')
        vRows = vTable.find_elements_by_tag_name('tr')
        self.assertIn('1: ��һЩ��ȸ��ë', [ vRow.text for vRow in vRows ])
        
        
        # ����ڶ�����������
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        vInputBox.send_keys('�ÿ�ȸ��ë����Ӭ')
        vInputBox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # �ٴβ鿴�ո�����Ĵ�������
        vTable = self.vBrowser.find_element_by_id('id_list_table')
        vRows = vTable.find_elements_by_tag_name('tr')
        self.assertIn('1: ��һЩ��ȸ��ë',   [ vRow.text for vRow in vRows ])
        self.assertIn('2: �ÿ�ȸ��ë����Ӭ', [ vRow.text for vRow in vRows ])


        self.fail('Finish The Test!')



if (__name__ == '__main__'):
    #unittest.main(warnings='ignore')
    unittest.main()
