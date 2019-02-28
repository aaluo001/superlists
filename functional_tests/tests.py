#!python
# coding: gbk
#------------------------------
# tests.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
import os
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


# �ȴ���������Ӧʱ��(10��)
# 10�����Բ���Ǳ�ڵ�����Ͳ���Ԥ֪�Ļ�������
MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
  
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.getenv('STAGING_SERVER')
        if (staging_server): self.live_server_url = 'http://{}'.format(staging_server)
  
    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                list_table = self.browser.find_element_by_id('id_list_table')
                rows = list_table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [ row.text for row in rows ])
                break
            
            except (AssertionError, WebDriverException) as e:
                if ((time.time() - start_time) > MAX_WAIT): raise e
                time.sleep(1)


    def test_can_start_a_list_and_retrieve_it_later(self):
        # ����Ӧ����ҳ
        self.browser.get(self.live_server_url)
        
        # ҳ��ı���Ϳ�ͷ������ "To-Do" �����
        self.assertIn('��������', self.browser.title)
        self.assertIn('��������', self.browser.find_element_by_tag_name('h1').text)
        
        # ҳ����һ�����������ı������
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), '��������һ�����������')
        
        
        # �����һ����������
        input_box.send_keys('��һЩ��ȸ��ë')
        input_box.send_keys(Keys.ENTER)
        
        # �鿴�ո�����Ĵ�������
        self.wait_for_row_in_list_table('1: ��һЩ��ȸ��ë')
        

        # ����ڶ�����������
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('�ÿ�ȸ��ë����Ӭ')
        input_box.send_keys(Keys.ENTER)
        
        # �ٴβ鿴�ո�����Ĵ�������
        self.wait_for_row_in_list_table('1: ��һЩ��ȸ��ë')
        self.wait_for_row_in_list_table('2: �ÿ�ȸ��ë����Ӭ')

        # �������


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # �û�A�½���һ����������
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('��һЩ��ȸ��ë')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: ��һЩ��ȸ��ë')
        
        #����ʱ���û�A���Լ�Ψһ��URL
        user_url_1 = self.browser.current_url
        self.assertRegex(user_url_1, '/lists/.+/')
        
        # �û�A�ر��˻Ự
        self.browser.quit()
        
        # �û�B������һ���»Ự
        self.browser = webdriver.Firefox()
        
        # �û�B��ʼ�����嵥��ҳ
        # ҳ���п������û�A���嵥
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('��һЩ��ȸ��ë', page_text)
        self.assertNotIn('����Ӭ', page_text)
        
        # �û�B�½���һ����������
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('��һ��ţ��')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: ��һ��ţ��')
        
        # �û�B������Լ�Ψһ��URL
        user_url_2 = self.browser.current_url
        self.assertRegex(user_url_2, '/lists/.+/')
        self.assertNotEqual(user_url_1, user_url_2)
        
        # �û�B�������û�A���嵥
        # ֻ�ܿ����Լ����嵥
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('��һЩ��ȸ��ë', page_text)
        self.assertIn('��һ��ţ��', page_text)

        # �������


    def test_layout_and_styling(self):
        # ����Ӧ����ҳ
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        
        # ����������ʾ
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual( \
            input_box.location['x'] + input_box.size['width'] / 2, \
            512, \
            delta=10 \
        )
        
        input_box.send_keys('testing')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        
        # ����������ʾ
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual( \
            input_box.location['x'] + input_box.size['width'] / 2, \
            512, \
            delta=10 \
        )

