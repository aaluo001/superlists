#!python
# coding: gbk
#------------------------------
# test_login.py
#------------------------------
# author: TangJianwei
# update: 2019-03-23
#------------------------------
import re
from django.core import mail

from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


TEST_EMAIL = 'aaluo008@163.com'
SUBJECT = '[from superlists]登录验证'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_login(self):
        # 访问应用首页
        # 发现导航栏中的登录区域
        # 于是，输入电子邮件地址
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(TEST_EMAIL)
        input_email.send_keys(Keys.ENTER)
        
        # 出现一天消息，表示电子邮件已经发出去了
        self.wait_for(lambda: self.assertIn(
            '电子邮件发送成功',
            self.browser.find_element_by_tag_name('body').text
        ))
        
        # 查看电子邮件
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(SUBJECT, email.subject)
        
        # 邮件中有个URL链接
        self.assertIn('请使用下面的链接进行登录验证', email.body)
        url_search = re.search('http://.+/accounts/login\?uid=.+$', email.body)
        if (not url_search):
            self.fail('Could not find url in email body: \n{}'.format(email.body))
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        
        # 点击链接
        self.browser.get(url)
        
        # 登录成功
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Log out')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

