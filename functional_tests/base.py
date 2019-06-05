#!python
# coding: gbk
#------------------------------
# functional_tests.base
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
import os
import re
import time
import poplib

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.core import mail
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings

from .server_tools import STAGING_SERVER, reset_database, create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


# 等待服务器响应时间(10秒)
# 10秒足以捕获潜在的问题和不可预知的缓慢因素
MAX_WAIT = 10

def wait(func):
    def modified_func(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return func(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if ((time.time() - start_time) > MAX_WAIT): raise e
                time.sleep(0.5)
    return modified_func


class FunctionalTest(StaticLiveServerTestCase):
    ''' 功能测试（基类）
    '''
    def init_browser(self):
        self.browser = webdriver.Firefox()
        #self.browser = webdriver.PhantomJS()
    
    def quit_browser(self):
        try:
            self.browser.quit()
        except:
            pass

        
    def setUp(self):
        self.init_browser()

        self.staging_tests = False
        if (os.getenv('STAGING_TESTS') == 'yes'):
            self.staging_tests = True
        
        if (self.staging_tests):
            self.live_server_url = 'http://' + STAGING_SERVER
            reset_database()

    def tearDown(self):
        self.quit_browser()

        
    def create_pre_authenticated_session(self, email):
        if (self.staging_tests):
            session_key = create_session_on_server(email)
        else:
            session_key = create_pre_authenticated_session(email)
        
        # 为了设定Cookie，我们要先访问网站
        # 而404页面加载最快
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

        
    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def add_list_item(self, item_text):
        num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(num_rows+1, item_text)


    @wait
    def wait_for(self, func):
        return func()

    @wait
    def wait_for_row_in_list_table(self, row_num, row_text):
        list_table = self.browser.find_element_by_id('id_list_table')
        row = list_table.find_element_by_id('id_row_{}'.format(row_num))
        self.assertEqual(row_text, row.text)

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

        
        