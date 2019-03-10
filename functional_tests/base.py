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


# 等待服务器响应时间(10秒)
# 10秒足以捕获潜在的问题和不可预知的缓慢因素
MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
  
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.getenv('STAGING_SERVER')
        if (staging_server): self.live_server_url = 'http://{}'.format(staging_server)
  
    def tearDown(self):
        #self.browser.refresh()
        #self.browser.quit()
        self.browser.close()


    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                list_table = self.browser.find_element_by_id('id_list_table')
                rows = list_table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [ row.text for row in rows ])
                break
            
            except (AssertionError, WebDriverException) as e:
                if ((time.time() - start_time) > MAX_WAIT): raise e
                time.sleep(1)


    def wait_for(self, func):
        start_time = time.time()
        while True:
            try:
                return func()
            except (AssertionError, WebDriverException) as e:
                if ((time.time() - start_time) > MAX_WAIT): raise e
                time.sleep(1)


    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

