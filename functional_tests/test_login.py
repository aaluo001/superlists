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


TEST_EMAIL = 'abc@163.com'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_login(self):
        # 访问应用首页
        # 发现导航栏中的登录区域
        # 于是，输入电子邮件地址
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(TEST_EMAIL)
        input_email.send_keys(Keys.ENTER)
        
        # 出现一条消息，表示电子邮件已经发出去了
        self.wait_for(lambda: self.assertIn(
            '邮件发送成功',
            self.browser.find_element_by_tag_name('body').text
        ))
        
        # 查看电子邮件
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertIn('我们给您发送了一条登录验证用的链接', email.subject)
        self.assertIn('为此我们给您发送了一条链接，您可以使用这条链接进行登录', email.body)

        # 邮件中有个URL链接
        url_search = re.search('http://.+/accounts/login\?token=.+$', email.body)
        if (not url_search):
            self.fail('Could not find url in email body: \n{}'.format(email.body))
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        
        # 点击链接
        self.browser.get(url)
        
        # 登录成功
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # 退出登录
        self.browser.find_element_by_link_text('退出').click()

        # 退出成功
        self.wait_to_be_logged_out(email=TEST_EMAIL)

