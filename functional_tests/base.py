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
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


# �ȴ���������Ӧʱ��(10��)
# 10�����Բ���Ǳ�ڵ�����Ͳ���Ԥ֪�Ļ�������
MAX_WAIT = 10

# ���ɷ�����
STAGING_SERVER = 'http://tjw-superlists-staging.site'


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
        self.staging_tests = os.getenv('STAGING_TESTS')
        if (self.staging_tests):
            self.live_server_url = STAGING_SERVER
  
    def tearDown(self):
        #self.browser.refresh()
        #self.browser.quit()
        self.browser.close()


    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')


    @wait
    def wait_for(self, func):
        return func

    @wait
    def wait_for_row_in_list_table(self, row_text):
        list_table = self.browser.find_element_by_id('id_list_table')
        rows = list_table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [ row.text for row in rows ])

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('�˳�')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

