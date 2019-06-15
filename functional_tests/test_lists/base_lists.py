#------------------------------
# functional_tests.test_lists.base_lists
#------------------------------
# Author: TangJianwei
# Create: 2019-06-15
#------------------------------
from selenium.webdriver.common.keys import Keys

from functional_tests.base import wait
from functional_tests.base import FunctionalTest


class ListsTest(FunctionalTest):
    ''' 应用层功能测试（基类）
    '''
    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def add_list_item(self, item_text):
        num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(num_rows+1, item_text)

    @wait
    def wait_for_row_in_list_table(self, row_num, row_text):
        list_table = self.browser.find_element_by_id('id_list_table')
        row = list_table.find_element_by_id('id_row_{}'.format(row_num))
        self.assertEqual(row_text, row.text)

