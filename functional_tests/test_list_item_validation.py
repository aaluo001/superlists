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
        # ����������������û���������ݣ�ֱ�Ӱ��˻س���
        self.browser.get(self.live_server_url)
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # ������ػ�������ҳ�治�ᱻ����
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))
        
        # ����һЩ���ֺ󣬴�����ʾ��ʧ��
        input_box = self.get_item_input_box()
        input_box.send_keys('��һ��ţ��')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))

        # �����ύ�˸ô�������
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: ��һ��ţ��')


        # �����ֲ�С���ύ��һ���յĴ�������
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # ͬ������������ػ���
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # ������һЩ���ֺ󣬴�����ʾ��ʧ��
        input_box = self.get_item_input_box()
        input_box.send_keys('�ݱ���')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))

        # �����ύ�˸ô�������
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: ��һ��ţ��')
        self.wait_for_row_in_list_table('2: �ݱ���')

