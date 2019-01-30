#!python
# coding: gbk
# tests.py

import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.test import LiveServerTestCase


# �ȴ���������Ӧʱ��(10��)
# 10�����Բ���Ǳ�ڵ�����Ͳ���Ԥ֪�Ļ�������
MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
  
    def setUp(self):
        self.vBrowser = webdriver.Firefox()
  
    def tearDown(self):
        self.vBrowser.quit()

    def waitForRowInListTable(self, vRowText):
        vStartTime = time.time()
        while True:
            try:
                vTable = self.vBrowser.find_element_by_id('id_list_table')
                vRows = vTable.find_elements_by_tag_name('tr')
                self.assertIn(vRowText, [ vRow.text for vRow in vRows ])
                break
            
            except (AssertionError, WebDriverException) as e:
                if ((time.time() - vStartTime) > MAX_WAIT): raise e
                time.sleep(1)


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
        
        # �鿴�ո�����Ĵ�������
        self.waitForRowInListTable('1: ��һЩ��ȸ��ë')
        

        # ����ڶ�����������
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        vInputBox.send_keys('�ÿ�ȸ��ë����Ӭ')
        vInputBox.send_keys(Keys.ENTER)
        
        # �ٴβ鿴�ո�����Ĵ�������
        self.waitForRowInListTable('1: ��һЩ��ȸ��ë')
        self.waitForRowInListTable('2: �ÿ�ȸ��ë����Ӭ')


        self.fail('Finish The Test!')


    def test_MultipleUsersCanStartListsAtDifferentUrls(self):
        # �û�A�½���һ����������
        self.vBrowser.get(self.live_server_url)
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        vInputBox.send_keys('��һЩ��ȸ��ë')
        vInputBox.send_keys(Keys.ENTER)
        self.waitForRowInListTable('1: ��һЩ��ȸ��ë')
        
        #����ʱ���û�A���Լ�Ψһ��URL
        vUserAUrl = self.vBrowser.current_url
        self.assertRegex(vUserAUrl, '/lists/.+/')
        
        # �û�A�ر��˻Ự
        self.vBrowser.quit()
        
        # �û�B������һ���»Ự
        self.vBrowser = webdriver.Firefox()
        
        # �û�B��ʼ�����嵥��ҳ
        # ҳ���п������û�A���嵥
        self.vBrowser.get(self.live_server_url)
        vPageText = self.vBrowser.find_element_by_tag_name('body').text
        self.assertNotIn('��һЩ��ȸ��ë', vPageText)
        self.assertNotIn('����Ӭ', vPageText)
        
        # �û�B�½���һ����������
        vInputBox = self.vBrowser.find_element_by_id('id_new_item')
        vInputBox.send_keys('��һ��ţ��')
        vInputBox.send_keys(Keys.ENTER)
        self.waitForRowInListTable('1: ��һ��ţ��')
        
        # �û�B������Լ�Ψһ��URL
        vUserBUrl = self.vBrowser.current_url
        self.assertRegex(vUserBUrl, '/lists/.+/')
        self.assertNotEqual(vUserAUrl, vUserBUrl)
        
        # �û�B�������û�A���嵥
        # ֻ�ܿ����Լ����嵥
        vPageText = self.vBrowser.find_element_by_tag_name('body').text
        self.assertNotIn('��һЩ��ȸ��ë', vPageText)
        self.assertIn('��һ��ţ��', vPageText)


