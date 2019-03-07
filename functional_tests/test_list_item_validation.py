#!python
# coding: gbk
#------------------------------
# test_list_item_validation.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from selenium.webdriver.common.keys import Keys
#from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # 打开浏览器，输入框中没有输入内容，直接按了回车键
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(Keys.ENTER)

        # 页面刷新后显示了一个错误消息
        # 提示待办事项不能为空
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            '你不能提交一个空的待办事项！'
        ))
        
        # 输入一些文字后再次提交
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('买一盒牛奶')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 买一盒牛奶')

        # 接下来又不小心提交了一个空的待办事项
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(Keys.ENTER)

        # 页面刷新后显示了一个类似的错误消息
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            '你不能提交一个空的待办事项！'
        ))

        # 然后输入一些文字后再次提交
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('泡杯茶')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 买一盒牛奶')
        self.wait_for_row_in_list_table('2: 泡杯茶')

