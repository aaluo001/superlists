#!python
# coding: gbk
#------------------------------
# functional_tests.test_remove_list
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class RemoveListTest(FunctionalTest):
    ''' ɾ���嵥����
    '''
    def test_001(self):
        ''' ɾ���嵥����ת��"�ҵ��嵥"ҳ��
            ��ɾ�����嵥�޷�����
        '''
        # ������¼�û�
        self.create_pre_authenticated_session('abc@163.com')

        # �½��嵥
        self.browser.get(self.live_server_url)
        self.add_list_item('��һЩ��ȸ��ë')
        self.add_list_item('�ÿ�ȸ��ë����Ӭ')
        # ȡ�õ�ǰURL
        url = self.browser.current_url
        
        # ɾ���嵥
        self.browser.find_element_by_link_text('ɾ���嵥').click()

        # Ǩ�Ƶ�"�ҵ��嵥"ҳ��
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('div.text-center > h1').text,
            '�ҵ��嵥'
        ))
        self.assertIn('/lists/', self.browser.current_url)
        
        # ɾ�����嵥�޷�����
        self.browser.get(url)
        self.wait_for(lambda: self.assertIn(
            'û���ҵ����嵥',
            self.browser.find_element_by_id('id_messages').text
        ))
        self.assertEqual(self.browser.current_url, self.live_server_url + '/')