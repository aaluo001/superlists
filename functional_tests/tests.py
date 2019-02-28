#!python
# coding: gbk
#------------------------------
# tests.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
import os
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


# 等待服务器响应时间(10秒)
# 10秒足以捕获潜在的问题和不可预知的缓慢因素
MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
  
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.getenv('STAGING_SERVER')
        if (staging_server): self.live_server_url = 'http://{}'.format(staging_server)
  
    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

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


    def test_can_start_a_list_and_retrieve_it_later(self):
        # 访问应用首页
        self.browser.get(self.live_server_url)
        
        # 页面的标题和开头都包含 "To-Do" 这个词
        self.assertIn('待办事项', self.browser.title)
        self.assertIn('待办事项', self.browser.find_element_by_tag_name('h1').text)
        
        # 页面有一个待办事项文本输入框
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), '试试输入一个待办事项吧')
        
        
        # 输入第一个待办事项
        input_box.send_keys('买一些孔雀羽毛')
        input_box.send_keys(Keys.ENTER)
        
        # 查看刚刚输入的待办事项
        self.wait_for_row_in_list_table('1: 买一些孔雀羽毛')
        

        # 输入第二个待办事项
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('用孔雀羽毛做假蝇')
        input_box.send_keys(Keys.ENTER)
        
        # 再次查看刚刚输入的待办事项
        self.wait_for_row_in_list_table('1: 买一些孔雀羽毛')
        self.wait_for_row_in_list_table('2: 用孔雀羽毛做假蝇')

        # 操作完毕


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 用户A新建了一个待办事项
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('买一些孔雀羽毛')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 买一些孔雀羽毛')
        
        #　这时，用户A有自己唯一的URL
        user_url_1 = self.browser.current_url
        self.assertRegex(user_url_1, '/lists/.+/')
        
        # 用户A关闭了会话
        self.browser.quit()
        
        # 用户B开启了一个新会话
        self.browser = webdriver.Firefox()
        
        # 用户B开始访问清单首页
        # 页面中看不到用户A的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('买一些孔雀羽毛', page_text)
        self.assertNotIn('做假蝇', page_text)
        
        # 用户B新建了一个待办事项
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('买一盒牛奶')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 买一盒牛奶')
        
        # 用户B获得了自己唯一的URL
        user_url_2 = self.browser.current_url
        self.assertRegex(user_url_2, '/lists/.+/')
        self.assertNotEqual(user_url_1, user_url_2)
        
        # 用户B看不到用户A的清单
        # 只能看到自己的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('买一些孔雀羽毛', page_text)
        self.assertIn('买一盒牛奶', page_text)

        # 操作完毕


    def test_layout_and_styling(self):
        # 访问应用首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        
        # 输入框居中显示
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual( \
            input_box.location['x'] + input_box.size['width'] / 2, \
            512, \
            delta=10 \
        )
        
        input_box.send_keys('testing')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        
        # 输入框居中显示
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual( \
            input_box.location['x'] + input_box.size['width'] / 2, \
            512, \
            delta=10 \
        )

