#!python
# coding: gbk
#------------------------------
# functional_tests.test_simple_list_creation
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
        self.assertIn('Superlists', self.browser.title)
        self.assertIn('�½��嵥', self.browser.find_element_by_tag_name('h1').text)
        
        # ҳ����һ�����������ı������
        input_box = self.get_item_input_box()
        self.assertEqual(input_box.get_attribute('placeholder'), '�����������')

        # �����һ����������
        self.add_list_item('��һЩ��ȸ��ë')
        # ����ڶ�����������
        self.add_list_item('�ÿ�ȸ��ë����Ӭ')

        # �������


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # �û�A�½���һ����������
        self.browser.get(self.live_server_url)
        self.add_list_item('��һЩ��ȸ��ë')

        
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
        self.add_list_item('��һ��ţ��')

        
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

