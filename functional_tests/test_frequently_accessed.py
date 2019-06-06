#!python
# coding: gbk
#------------------------------
# functional_tests.test_frequently_accessed
#------------------------------
# Author: TangJianwei
# Create: 2019-06-01
#------------------------------
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class FrequentlyAccessedTest(FunctionalTest):
    ''' Ƶ�����ʲ���
    '''
    def test_001(self):
        ''' ����ʱ�����ڶ�η��͵�¼��֤�ʼ�
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
 

        # �ڶ��η��͵�¼��֤�ʼ�
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # ����ʱ��������(5��)����ʾ��ϵͳ��æ������Ϣ
        self.wait_for(lambda: self.assertIn(
            'ϵͳ��æ',
            self.browser.find_element_by_id('id_messages').text
        ))

