#!python
# coding: gbk
#------------------------------
# functional_tests.test_new_list
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class NewListTest(FunctionalTest):
    ''' �½��嵥����
    '''
    def test_001(self):
        ''' �½��嵥
        '''
        # ����Ӧ����ҳ
        # ���Կ���ҳ����⣬�Լ���Ļ���½��嵥
        self.browser.get(self.live_server_url)
        self.assertIn('Superlists', self.browser.title)
        self.assertIn('�½��嵥', self.browser.find_element_by_tag_name('h1').text)

        # �����������
        self.add_list_item('��һЩ��ȸ��ë')
        self.add_list_item('�ÿ�ȸ��ë����Ӭ')


    def test_002(self):
        ''' �½���ͬ���嵥
        '''
        # �½���һ�����������嵥
        self.browser.get(self.live_server_url)
        self.add_list_item('��һЩ��ȸ��ë')
        list_url_1 = self.browser.current_url
        self.assertRegex(list_url_1, '/lists/.+/')
        
        # �ر������
        self.browser.quit()
        
        # ����һ�������
        # �½��ڶ������������嵥
        self.init_browser()
        self.browser.get(self.live_server_url)
        self.add_list_item('��һ��ţ��')
        list_url_2 = self.browser.current_url
        self.assertRegex(list_url_2, '/lists/.+/')
        
        # �����嵥��URL�ǲ�һ����
        self.assertNotEqual(list_url_1, list_url_2)
        
        # �Ҳ��ܿ�����һ���嵥������
        # ֻ�ܿ����Լ��嵥������
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('��һЩ��ȸ��ë', page_text)
        self.assertIn('��һ��ţ��', page_text)

