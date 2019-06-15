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
    ''' 输入框效验测试
    '''
    def test_001(self):
        ''' 首页和清单页面都不能提交空的待办事项
        '''
        self.browser.get(self.live_server_url)

        # 首页提交一个空的待办事项
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # 浏览器截获了请求，页面不会被加载
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:invalid')
        )
        
        # 输入待办事项后，错误消失了
        input_box = self.get_item_input_box()
        input_box.send_keys('买一盒牛奶')
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:valid')
        )

        # 提交待办事项，清单页面显示正常
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(1, '买一盒牛奶')


        # 清单页面又提交一个空的待办事项
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # 同样，被浏览器截获了
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:invalid')
        )

        # 输入待办事项后，错误消失了
        input_box = self.get_item_input_box()
        input_box.send_keys('泡杯茶')
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:valid')
        )

        # 提交待办事项，清单页面显示正常
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(1, '买一盒牛奶')
        self.wait_for_row_in_list_table(2, '泡杯茶')


    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')


    def test_002(self):
        ''' 不能提交重复的待办事项
        '''
        self.browser.get(self.live_server_url)
        self.add_list_item('买一盒牛奶')

        # 输入一个同样的待办事项
        input_box = self.get_item_input_box()
        input_box.send_keys('买一盒牛奶')
        input_box.send_keys(Keys.ENTER)

        # 于是，得到一条错误消息
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            '您已经提交一个同样的待办事项！'
        ))

        # 再次输入时，错误消息消失了
        input_box = self.get_item_input_box()
        input_box.send_keys('a')
        time.sleep(1)

        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))

