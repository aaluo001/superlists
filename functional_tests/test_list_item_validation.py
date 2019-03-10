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
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # 浏览器截获了请求，页面不会被加载
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))
        
        # 输入一些文字后，错误提示消失了
        input_box = self.get_item_input_box()
        input_box.send_keys('买一盒牛奶')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))

        # 于是提交了该待办事项
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 买一盒牛奶')


        # 接着又不小心提交了一个空的待办事项
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # 同样，被浏览器截获了
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # 再输入一些文字后，错误提示消失了
        input_box = self.get_item_input_box()
        input_box.send_keys('泡杯茶')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))

        # 于是提交了该待办事项
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 买一盒牛奶')
        self.wait_for_row_in_list_table('2: 泡杯茶')

