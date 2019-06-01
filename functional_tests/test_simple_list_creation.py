#!python
# coding: gbk
#------------------------------
# functional_tests.test_simple_list_creation
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 访问应用首页
        self.browser.get(self.live_server_url)
        
        # 页面的标题和开头都包含 "To-Do" 这个词
        self.assertIn('Superlists', self.browser.title)
        self.assertIn('新建清单', self.browser.find_element_by_tag_name('h1').text)
        
        # 页面有一个待办事项文本输入框
        input_box = self.get_item_input_box()
        self.assertEqual(input_box.get_attribute('placeholder'), '输入待办事项')

        # 输入第一个待办事项
        self.add_list_item('买一些孔雀羽毛')
        # 输入第二个待办事项
        self.add_list_item('用孔雀羽毛做假蝇')

        # 操作完毕


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 用户A新建了一个待办事项
        self.browser.get(self.live_server_url)
        self.add_list_item('买一些孔雀羽毛')

        
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
        input_box = self.get_item_input_box()
        self.add_list_item('买一盒牛奶')

        
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

