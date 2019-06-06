#!python
# coding: gbk
#------------------------------
# functional_tests.test_view_list
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ViewListTest(FunctionalTest):
    ''' ��ʾ�嵥����
    '''
    def test_001(self):
        ''' ͨ��URL��ʾ�嵥
        '''
        # �½��嵥
        self.browser.get(self.live_server_url)
        self.add_list_item('��һЩ��ȸ��ë')
        self.add_list_item('�ÿ�ȸ��ë����Ӭ')

        # ȡ�õ�ǰURL�����ر������
        url = self.browser.current_url
        self.quit_browser()
        
        # ͨ��URL����ʾ�嵥
        self.init_browser()
        self.browser.get(url)
        
        # ����֮ǰ����Ĵ�������
        self.wait_for(lambda: self.assertIn(
            '��һЩ��ȸ��ë',
            self.browser.find_element_by_id('id_list_table').text
        ))
        
        self.wait_for(lambda: self.assertIn(
            '�ÿ�ȸ��ë����Ӭ',
            self.browser.find_element_by_id('id_list_table').text
        ))

        