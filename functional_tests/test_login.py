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
            self.assertIn('我们给您发送了一条登录验证用的链接', email.subject)
            return email.body


    def test_can_get_email_link_to_login(self):
        # 访问应用首页
        # 发现导航栏中的登录区域
        # 于是，输入电子邮件地址
        test_email_password = None
        if (self.staging_tests):
            test_email = 'superlists_tests@163.com'
        else:
            test_email = 'abc@163.com'
        
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # 出现一条消息，表示电子邮件已经发出去了
        self.wait_for(lambda: self.assertIn(
            '邮件发送成功',
            self.browser.find_element_by_tag_name('body').text
        ))
        
        # 查看电子邮件
        email_body = self.wait_for_email(test_email)
        self.assertIn('为此我们给您发送了一条链接，您可以使用这条链接进行登录', email_body)

        # 邮件中有个URL链接
        url_search = re.search(r'http://.+/accounts/login\?token=.+', email_body)
        if (not url_search):
            self.fail('Could not find url in email body: \n{}'.format(email_body))
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        
        # 点击链接
        self.browser.get(url)

        # 登录成功
        self.wait_to_be_logged_in(email=test_email)

        # 退出登录
        self.browser.find_element_by_link_text('退出').click()

        # 退出成功
        self.wait_to_be_logged_out(email=test_email)

