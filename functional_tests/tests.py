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
        # ����Ӧ����ҳ
        self.vBrowser.get(self.live_server_url)
        
        # ҳ��ı���Ϳ�ͷ������ "To-Do" �����
        self.assertIn('��������', self.vBrowser.title)
        self.assertIn('��������', self.vBrowser.find_element_by_tag_name('h1').text)
        
        # ҳ����һ�����������ı������
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        self.assertEqual(vInputBox.get_attribute('placeholder'), '��������һ�����������')
        
        
        # �����һ����������
        vInputBox.send_keys('��һЩ��ȸ��ë')
        vInputBox.send_keys(Keys.ENTER)
        time.sleep(3)
        
        # �鿴�ո�����Ĵ�������
        self.checkForRowInListTable('1: ��һЩ��ȸ��ë')
        

        # ����ڶ�����������
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        vInputBox.send_keys('�ÿ�ȸ��ë����Ӭ')
        vInputBox.send_keys(Keys.ENTER)
        time.sleep(3)
        
        # �ٴβ鿴�ո�����Ĵ�������
        self.checkForRowInListTable('1: ��һЩ��ȸ��ë')
        self.checkForRowInListTable('2: �ÿ�ȸ��ë����Ӭ')


        self.fail('Finish The Test!')

