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
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(Keys.ENTER)

        # ҳ��ˢ�º���ʾ��һ��������Ϣ
        # ��ʾ���������Ϊ��
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            '�㲻���ύһ���յĴ������'
        ))
        
        # ����һЩ���ֺ��ٴ��ύ
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('��һ��ţ��')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: ��һ��ţ��')

        # �������ֲ�С���ύ��һ���յĴ�������
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(Keys.ENTER)

        # ҳ��ˢ�º���ʾ��һ�����ƵĴ�����Ϣ
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            '�㲻���ύһ���յĴ������'
        ))

        # Ȼ������һЩ���ֺ��ٴ��ύ
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('�ݱ���')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: ��һ��ţ��')
        self.wait_for_row_in_list_table('2: �ݱ���')

