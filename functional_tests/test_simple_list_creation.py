#!python
# coding: gbk
#------------------------------
# test_simple_list_creation.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # ����Ӧ����ҳ
        self.browser.get(self.live_server_url)
        
        # ҳ��ı���Ϳ�ͷ������ "To-Do" �����
        self.assertIn('��������', self.browser.title)
        self.assertIn('��������', self.browser.find_element_by_tag_name('h1').text)
        
        # ҳ����һ�����������ı������
        input_box = self.get_item_input_box()
        self.assertEqual(input_box.get_attribute('placeholder'), '�½�һ����������')
        
        
        # �����һ����������
        input_box.send_keys('��һЩ��ȸ��ë')
        input_box.send_keys(Keys.ENTER)
        
        # �鿴�ո�����Ĵ�������
        self.wait_for_row_in_list_table('1: ��һЩ��ȸ��ë')
        

        # ����ڶ�����������
        input_box = self.get_item_input_box()
        input_box.send_keys('�ÿ�ȸ��ë����Ӭ')
        input_box.send_keys(Keys.ENTER)
        
        # �ٴβ鿴�ո�����Ĵ�������
        self.wait_for_row_in_list_table('1: ��һЩ��ȸ��ë')
        self.wait_for_row_in_list_table('2: �ÿ�ȸ��ë����Ӭ')

        # �������


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # �û�A�½���һ����������
        self.browser.get(self.live_server_url)
        input_box = self.get_item_input_box()
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
        input_box = self.get_item_input_box()
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

