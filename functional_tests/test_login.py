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
    ''' 登录测试
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
            # 第二次发送邮件时，len(mail.outbox) == 2
            #self.assertEqual(len(mail.outbox), 1)
            email = mail.outbox[-1]
            self.assertIn(test_email, email.to)
            #self.assertIn('我们给您发送了一条登录验证的链接', email.subject)
            return email.body


    def test_001(self):
        ''' 输入邮箱地址发送邮件，然后取得登录验证的链接并成功登录
        '''
        if (self.staging_tests):
            test_email = 'superlists_tests@163.com'
        else:
            test_email = 'abc@163.com'
        
        # 访问首页
        # 在导航栏的登录区域输入邮箱地址
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # 检测到“邮件发送成功”的消息
        self.wait_for(lambda: self.assertIn(
            '邮件发送成功',
            self.browser.find_element_by_tag_name('body').text
        ))

        # 查看邮件内容
        email_body = self.wait_for_email(test_email)
        #self.assertIn('为此我们给您发送了一条链接，您可以使用这条链接进行登录', email_body)

        # 找到登录验证的链接
        url_search = re.search(r'http://.+/accounts/login\?token=.+', email_body)
        if (not url_search):
            self.fail('Could not find url in email body: \n{}'.format(email_body))
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 使用链接进行登录
        self.browser.get(url)
        self.wait_to_be_logged_in(email=test_email)

        # 退出
        self.browser.find_element_by_link_text('退出').click()
        self.wait_to_be_logged_out(email=test_email)


    def test_002(self):
        ''' 使用错误的链接无法完成登录，并得到登录失败的提示
        '''
        # 使用错误的链接访问网站
        discorrect_url = '{}/accounts/login?token=abc123'.format(self.live_server_url)
        self.browser.get(discorrect_url)

        # 检测到“登录失败”的消息
        self.wait_for(lambda: self.assertIn(
            '登录失败',
            self.browser.find_element_by_tag_name('body').text
        ))
        # 检测到邮箱地址的输入框
        self.browser.find_element_by_name('email')


    def test_003(self):
        ''' 对同一邮箱地址发送了两次登录验证的邮件
            那么，第一次得到的登录验证邮件中的链接无法完成登录
            第二次得到的则可以
        '''
        if (self.staging_tests):
            test_email = 'superlists_tests@163.com'
        else:
            test_email = 'abc@163.com'

        # 第一次发送登录验证邮件
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # 检测到“邮件发送成功”的消息
        self.wait_for(lambda: self.assertIn(
            '邮件发送成功',
            self.browser.find_element_by_tag_name('body').text
        ))

        # 查看邮件内容，并得到第一个链接
        email_body = self.wait_for_email(test_email)
        url_search = re.search(r'http://.+/accounts/login\?token=.+', email_body)
        if (not url_search):
            self.fail('Could not find url-1 in email body: \n{}'.format(email_body))
        url_1 = url_search.group(0)

 
        # 第二次发送登录验证邮件
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # 检测到“邮件发送成功”的消息
        self.wait_for(lambda: self.assertIn(
            '邮件发送成功',
            self.browser.find_element_by_tag_name('body').text
        ))

        # 查看邮件内容，并得到第二个链接
        email_body = self.wait_for_email(test_email)
        url_search = re.search(r'http://.+/accounts/login\?token=.+', email_body)
        if (not url_search):
            self.fail('Could not find url-2 in email body: \n{}'.format(email_body))
        url_2 = url_search.group(0)


        # 两个链接是不一样的
        self.assertNotEqual(url_1, url_2)

        # 使用第一个链接
        self.browser.get(url_1)

        # 检测到“登录失败”的消息
        self.wait_for(lambda: self.assertIn(
            '登录失败',
            self.browser.find_element_by_tag_name('body').text
        ))
        # 检测到邮箱地址的输入框
        self.browser.find_element_by_name('email')


        # 使用第二个链接，成功登录
        self.browser.get(url_2)
        self.wait_to_be_logged_in(email=test_email)

