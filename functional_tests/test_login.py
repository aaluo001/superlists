#!python
# coding: gbk
#------------------------------
# functional_tests.test_login
#------------------------------
# Author: TangJianwei
# Create: 2019-03-23
#------------------------------
import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LoginTest(FunctionalTest):
    ''' ��¼����
    '''
    def test_001(self):
        ''' ���������ַ�����ʼ���Ȼ��ȡ�õ�¼��֤�����Ӳ��ɹ���¼
        '''
        if (self.staging_tests):
            test_email = 'superlists_tests@163.com'
        else:
            test_email = 'abc@163.com'
        
        # ������ҳ
        # �ڵ������ĵ�¼�������������ַ
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # ��⵽���ʼ����ͳɹ�������Ϣ
        self.wait_for(lambda: self.assertIn(
            '�ʼ����ͳɹ�',
            self.browser.find_element_by_id('id_messages').text
        ))

        # �鿴�ʼ����ݣ����ҵ���¼��֤������
        email_body = self.wait_for_email(test_email)
        url = self.get_token_url(email_body)
        self.assertIn(self.live_server_url, url)

        # ʹ�����ӽ��е�¼
        self.browser.get(url)
        self.wait_to_be_logged_in(email=test_email)

        # �˳�
        self.browser.find_element_by_link_text('�˳�').click()
        self.wait_to_be_logged_out(email=test_email)


    def test_002(self):
        ''' ʹ�ô���������޷���ɵ�¼�����õ���¼ʧ�ܵ���ʾ
        '''
        # ʹ�ô�������ӷ�����վ
        discorrect_url = '{}/accounts/login?token=abc123'.format(self.live_server_url)
        self.browser.get(discorrect_url)

        # ��⵽����¼ʧ�ܡ�����Ϣ
        self.wait_for(lambda: self.assertIn(
            '��¼ʧ��',
            self.browser.find_element_by_id('id_messages').text
        ))
        # ��⵽�����ַ�������
        self.browser.find_element_by_name('email')


    def test_003(self):
        ''' ��ͬһ�����ַ���������ε�¼��֤���ʼ�
            ��ô����һ�εõ��ĵ�¼��֤�ʼ��е������޷���ɵ�¼
            �ڶ��εõ��������
        '''
        if (self.staging_tests):
            test_email = 'superlists_tests@163.com'
        else:
            test_email = 'abc@163.com'

        # ��һ�η��͵�¼��֤�ʼ�
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # ��⵽���ʼ����ͳɹ�������Ϣ
        self.wait_for(lambda: self.assertIn(
            '�ʼ����ͳɹ�',
            self.browser.find_element_by_id('id_messages').text
        ))

        # �鿴�ʼ����ݣ����õ���һ������
        email_body = self.wait_for_email(test_email)
        url_1 = self.get_token_url(email_body)
        self.browser.quit()

        
        # ������������
        time.sleep(5)
 
        # �ڶ��η��͵�¼��֤�ʼ�
        self.init_browser()
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # ��⵽���ʼ����ͳɹ�������Ϣ
        self.wait_for(lambda: self.assertIn(
            '�ʼ����ͳɹ�',
            self.browser.find_element_by_id('id_messages').text
        ))

        # �鿴�ʼ����ݣ����õ��ڶ�������
        email_body = self.wait_for_email(test_email)
        url_2 = self.get_token_url(email_body)


        # ���������ǲ�һ����
        self.assertNotEqual(url_1, url_2)

        # ʹ�õ�һ������
        self.browser.get(url_1)

        # ��⵽����¼ʧ�ܡ�����Ϣ
        self.wait_for(lambda: self.assertIn(
            '��¼ʧ��',
            self.browser.find_element_by_id('id_messages').text
        ))
        # ��⵽�����ַ�������
        self.browser.find_element_by_name('email')


        # ʹ�õڶ������ӣ��ɹ���¼
        self.browser.get(url_2)
        self.wait_to_be_logged_in(email=test_email)

