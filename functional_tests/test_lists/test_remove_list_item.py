#------------------------------
# functional_tests.test_lists.test_remove_list_item
#------------------------------
# Author: TangJianwei
# Create: 2019-06-16
#------------------------------
from selenium.webdriver.common.keys import Keys

from .base_lists import ListsTest


class RemoveListItemTest(ListsTest):
    ''' 删除待办事项测试
    '''
    def test_001(self):
        ''' 待办事项删除按钮的活性与非活性
            第一条待办事项的删除按钮是非活性，其余均是活性
        '''
        # 创建登录用户
        self.create_pre_authenticated_session('abc@163.com')

        # 新建一条待办事项，并检查其活性与非活性
        self.browser.get(self.live_server_url)
        self.add_list_item('New item 1')

        remove_1 = self.browser.find_element_by_css_selector('button#id_remove_list_item_1')
        self.assertEqual(remove_1.text, '×')
        self.assertTrue(remove_1.get_attribute('disabled'))

        # 再新建两条待办事项，并检查其活性与非活性
        self.add_list_item('New item 2')
        self.add_list_item('New item 3')

        remove_1 = self.browser.find_element_by_css_selector('button#id_remove_list_item_1')
        self.assertEqual(remove_1.text, '×')
        self.assertTrue(remove_1.get_attribute('disabled'))

        remove_2 = self.browser.find_element_by_css_selector('button#id_remove_list_item_2')
        self.assertEqual(remove_2.text, '×')
        self.assertIsNone(remove_2.get_attribute('disabled'))

        remove_3 = self.browser.find_element_by_css_selector('button#id_remove_list_item_3')
        self.assertEqual(remove_3.text, '×')
        self.assertIsNone(remove_3.get_attribute('disabled'))


    def test_002(self):
        ''' 删除待办事项，并跳转到本页面
        '''
        # 创建登录用户
        self.create_pre_authenticated_session('abc@163.com')

        # 新建待办事项
        self.browser.get(self.live_server_url)
        self.add_list_item('New item 1')
        self.add_list_item('New item 2')
        url = self.browser.current_url

        # 删除待办事项
        self.browser.find_element_by_css_selector('button#id_remove_list_item_2').click()

        # 可以找到第一条待办事项
        self.wait_for_row_in_list_table(1, 'New item 1')
        
        remove_1 = self.browser.find_element_by_css_selector('button#id_remove_list_item_1')
        self.assertEqual(remove_1.text, '×')
        self.assertTrue(remove_1.get_attribute('disabled'))


        # 无法找到第二条待办事项
        list_table = self.browser.find_element_by_id('id_list_table')
        self.assertEqual(
            list_table.find_elements_by_id('id_row_2'),
            []
        )
        self.assertEqual(
            list_table.find_elements_by_id('button#id_remove_list_item_2'),
            []
        )


    def test_003(self):
        ''' 匿名用户看不到删除按钮
        '''
        # 新建待办事项
        self.browser.get(self.live_server_url)
        self.add_list_item('New item 1')
        self.add_list_item('New item 2')

        self.assertEqual(
            self.browser.find_elements_by_css_selector('button#id_remove_list_item_1'),
            []
        )
        self.assertEqual(
            self.browser.find_elements_by_css_selector('button#id_remove_list_item_2'),
            []
        )

