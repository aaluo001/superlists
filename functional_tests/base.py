#!python
# coding: gbk
#------------------------------
# base.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .server_tools import STAGING_SERVER, reset_database


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
  
    def setUp(self):
        self.browser = webdriver.Firefox()
        
        self.staging_tests = False
        if (os.getenv('STAGING_TESTS') == 'yes'):
            self.staging_tests = True
        
        if (self.staging_tests):
            self.live_server_url = 'http://' + STAGING_SERVER
            reset_database()


    def tearDown(self):
        #self.browser.refresh()
        #self.browser.quit()
        self.browser.close()


    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')


    @wait
    def wait_for(self, func):
        return func()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        list_table = self.browser.find_element_by_id('id_list_table')
        rows = list_table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [ row.text for row in rows ])

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


    def add_list_item(self, item_text):
        num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('{}: {}'.format(num_rows+1, item_text))

