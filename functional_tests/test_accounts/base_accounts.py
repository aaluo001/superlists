#------------------------------
# functional_tests.test_accounts.base_accounts
#------------------------------
# Author: TangJianwei
# Create: 2019-06-15
#------------------------------
import os
import re
import time
import poplib

from django.core import mail

from functional_tests.base import wait
from functional_tests.base import FunctionalTest


class AccountsTest(FunctionalTest):
    ''' 应用层功能测试（基类）
    '''
    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('退出')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)


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
                        #print('getting email: {}'.format(i))
                        _, lines, _ = inbox.retr(i)
                        lines = [ line.decode('utf-8') for line in lines ]
                        #print('email lines:')
                        #print(lines)
                        if ('From: superlists@163.com' in lines):
                            try: inbox.dele(i)
                            except: pass
                            email_body = '\n'.join(lines)
                            return email_body
                    time.sleep(5)
            finally:
                inbox.quit()
        
        else:
            # 第二次发送邮件时，len(mail.outbox) == 2
            #self.assertEqual(len(mail.outbox), 1)
            email = mail.outbox[-1]
            self.assertIn(test_email, email.to)
            #self.assertIn('xxx', email.subject)
            return email.body

    def get_token_url(self, email_body):
        url_search = re.search(r'http://.+/accounts/login\?token=.+', email_body)
        if (not url_search):
            self.fail('Could not find url in email body: \n{}'.format(email_body))
        return url_search.group(0)

