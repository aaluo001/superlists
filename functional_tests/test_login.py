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
    ''' 登录测试
    '''
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
            self.browser.find_element_by_id('id_messages').text
        ))

        # 查看邮件内容，并找到登录验证的链接
        email_body = self.wait_for_email(test_email)
        url = self.get_token_url(email_body)
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
            self.browser.find_element_by_id('id_messages').text
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
            self.browser.find_element_by_id('id_messages').text
        ))

        # 查看邮件内容，并得到第一个链接
        email_body = self.wait_for_email(test_email)
        url_1 = self.get_token_url(email_body)
        self.browser.quit()

        
        # 规避爬虫监测程序
        time.sleep(5)
 
        # 第二次发送登录验证邮件
        self.init_browser()
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # 检测到“邮件发送成功”的消息
        self.wait_for(lambda: self.assertIn(
            '邮件发送成功',
            self.browser.find_element_by_id('id_messages').text
        ))

        # 查看邮件内容，并得到第二个链接
        email_body = self.wait_for_email(test_email)
        url_2 = self.get_token_url(email_body)


        # 两个链接是不一样的
        self.assertNotEqual(url_1, url_2)

        # 使用第一个链接
        self.browser.get(url_1)

        # 检测到“登录失败”的消息
        self.wait_for(lambda: self.assertIn(
            '登录失败',
            self.browser.find_element_by_id('id_messages').text
        ))
        # 检测到邮箱地址的输入框
        self.browser.find_element_by_name('email')


        # 使用第二个链接，成功登录
        self.browser.get(url_2)
        self.wait_to_be_logged_in(email=test_email)

