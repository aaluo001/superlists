#!python
# coding: gbk
#------------------------------
# functional_tests.test_login
#------------------------------
# Author: TangJianwei
# Create: 2019-03-23
#------------------------------
import os
import re
import time
import poplib

from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LoginTest(FunctionalTest):
    ''' ��¼����
    '''
    def wait_for_email(self, test_email):
        if (self.staging_tests):
            inbox = poplib.POP3_SSL('pop.163.com')
            try:
                inbox.user(test_email)
                inbox.pass_(os.environ['TEST_EMAIL_PASSWORD'])
                start_time = time.time()
                
                while (time.time() - start_time) < 60:
                    email_count, _ = inbox.stat()
                    for i in reversed(range(max(1, email_count-10), email_count+1)):
                        print('getting email: {}'.format(i))
                        _, lines, _ = inbox.retr(i)
                        lines = [ line.decode('utf-8') for line in lines ]
                        print('email lines:')
                        print(lines)
                        if ('From: superlists@163.com' in lines):
                            try: inbox.dele(i)
                            except: pass
                            email_body = '\n'.join(lines)
                            return email_body
                    time.sleep(5)
            finally:
                inbox.quit()
            
        else:
            # �ڶ��η����ʼ�ʱ��len(mail.outbox) == 2
            #self.assertEqual(len(mail.outbox), 1)
            email = mail.outbox[-1]
            self.assertIn(test_email, email.to)
            #self.assertIn('���Ǹ���������һ����¼��֤������', email.subject)
            return email.body


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
            self.browser.find_element_by_tag_name('body').text
        ))

        # �鿴�ʼ�����
        email_body = self.wait_for_email(test_email)
        #self.assertIn('Ϊ�����Ǹ���������һ�����ӣ�������ʹ���������ӽ��е�¼', email_body)

        # �ҵ���¼��֤������
        url_search = re.search(r'http://.+/accounts/login\?token=.+', email_body)
        if (not url_search):
            self.fail('Could not find url in email body: \n{}'.format(email_body))
        url = url_search.group(0)
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
            self.browser.find_element_by_tag_name('body').text
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
            self.browser.find_element_by_tag_name('body').text
        ))

        # �鿴�ʼ����ݣ����õ���һ������
        email_body = self.wait_for_email(test_email)
        url_search = re.search(r'http://.+/accounts/login\?token=.+', email_body)
        if (not url_search):
            self.fail('Could not find url-1 in email body: \n{}'.format(email_body))
        url_1 = url_search.group(0)

 
        # �ڶ��η��͵�¼��֤�ʼ�
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # ��⵽���ʼ����ͳɹ�������Ϣ
        self.wait_for(lambda: self.assertIn(
            '�ʼ����ͳɹ�',
            self.browser.find_element_by_tag_name('body').text
        ))

        # �鿴�ʼ����ݣ����õ��ڶ�������
        email_body = self.wait_for_email(test_email)
        url_search = re.search(r'http://.+/accounts/login\?token=.+', email_body)
        if (not url_search):
            self.fail('Could not find url-2 in email body: \n{}'.format(email_body))
        url_2 = url_search.group(0)


        # ���������ǲ�һ����
        self.assertNotEqual(url_1, url_2)

        # ʹ�õ�һ������
        self.browser.get(url_1)

        # ��⵽����¼ʧ�ܡ�����Ϣ
        self.wait_for(lambda: self.assertIn(
            '��¼ʧ��',
            self.browser.find_element_by_tag_name('body').text
        ))
        # ��⵽�����ַ�������
        self.browser.find_element_by_name('email')


        # ʹ�õڶ������ӣ��ɹ���¼
        self.browser.get(url_2)
        self.wait_to_be_logged_in(email=test_email)

