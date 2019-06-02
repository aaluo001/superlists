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
    ''' 频繁访问测试
    '''
    def test_001(self):
        ''' 连续时间间隔(5秒)内多次发送登录验证邮件
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
            self.browser.find_element_by_id('id_messages').text
        ))

        # 查看邮件内容，并得到第一个链接
        email_body = self.wait_for_email(test_email)
        url_1 = self.get_token_url(email_body)
 

        # 第二次发送登录验证邮件
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # 由于时间间隔不够(5秒)，提示“系统繁忙”的消息
        self.wait_for(lambda: self.assertIn(
            '系统繁忙',
            self.browser.find_element_by_id('id_messages').text
        ))

        # 查看邮件内容，并得到第二个链接
        email_body = self.wait_for_email(test_email)
        url_2 = self.get_token_url(email_body)


        # 两个链接是一样的
        self.assertEqual(url_1, url_2)

        # 使用第一个链接，成功登录
        self.browser.get(url_1)
        self.wait_to_be_logged_in(email=test_email)

