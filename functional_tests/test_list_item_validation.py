#!python
# coding: gbk
#------------------------------
# functional_tests.test_list_item_validation
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
import time
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ListItemValidationTest(FunctionalTest):
    ''' �����Ч�����
    '''
    def test_001(self):
        ''' ��ҳ���嵥ҳ�涼�����ύ�յĴ�������
        '''
        self.browser.get(self.live_server_url)

        # ��ҳ�ύһ���յĴ�������
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # ������ػ�������ҳ�治�ᱻ����
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:invalid')
        )
        
        # �����������󣬴�����ʧ��
        input_box = self.get_item_input_box()
        input_box.send_keys('��һ��ţ��')
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:valid')
        )

        # �ύ��������嵥ҳ����ʾ����
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(1, '��һ��ţ��')


        # �嵥ҳ�����ύһ���յĴ�������
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # ͬ������������ػ���
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:invalid')
        )

        # �����������󣬴�����ʧ��
        input_box = self.get_item_input_box()
        input_box.send_keys('�ݱ���')
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:valid')
        )

        # �ύ��������嵥ҳ����ʾ����
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(1, '��һ��ţ��')
        self.wait_for_row_in_list_table(2, '�ݱ���')


    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')


    def test_002(self):
        ''' �����ύ�ظ��Ĵ�������
        '''
        self.browser.get(self.live_server_url)
        self.add_list_item('��һ��ţ��')

        # ����һ��ͬ���Ĵ�������
        input_box = self.get_item_input_box()
        input_box.send_keys('��һ��ţ��')
        input_box.send_keys(Keys.ENTER)

        # ���ǣ��õ�һ��������Ϣ
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            '���Ѿ��ύһ��ͬ���Ĵ������'
        ))

        # �ٴ�����ʱ��������Ϣ��ʧ��
        input_box = self.get_item_input_box()
        input_box.send_keys('a')
        time.sleep(1)

        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))

