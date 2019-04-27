#!python
# coding: gbk
#------------------------------
# test_login.py
#------------------------------
# author: TangJianwei
# update: 2019-03-23
#------------------------------
import os
import re
import time
import poplib

from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LoginTest(FunctionalTest):

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
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertIn('���Ǹ���������һ����¼��֤�õ�����', email.subject)
            return email.body


    def test_can_get_email_link_to_login(self):
        # ����Ӧ����ҳ
        # ���ֵ������еĵ�¼����
        # ���ǣ���������ʼ���ַ
        test_email_password = None
        if (self.staging_tests):
            test_email = 'superlists_tests@163.com'
        else:
            test_email = 'abc@163.com'
        
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # ����һ����Ϣ����ʾ�����ʼ��Ѿ�����ȥ��
        self.wait_for(lambda: self.assertIn(
            '�ʼ����ͳɹ�',
            self.browser.find_element_by_tag_name('body').text
        ))
        
        # �鿴�����ʼ�
        email_body = self.wait_for_email(test_email)
        self.assertIn('Ϊ�����Ǹ���������һ�����ӣ�������ʹ���������ӽ��е�¼', email_body)

        # �ʼ����и�URL����
        url_search = re.search(r'http://.+/accounts/login\?token=.+', email_body)
        if (not url_search):
            self.fail('Could not find url in email body: \n{}'.format(email_body))
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        
        # �������
        self.browser.get(url)

        # ��¼�ɹ�
        self.wait_to_be_logged_in(email=test_email)

        # �˳���¼
        self.browser.find_element_by_link_text('�˳�').click()

        # �˳��ɹ�
        self.wait_to_be_logged_out(email=test_email)

