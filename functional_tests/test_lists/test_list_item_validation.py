#------------------------------
# functional_tests.test_lists.test_list_item_validation
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
import time

from selenium.webdriver.common.keys import Keys

from .base_lists import ListsTest


class ListItemValidationTest(ListsTest):
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
        self.assertEqual(
            self.get_error_element().text,
            '您已经提交一个同样的待办事项！'
        )

        # 再次输入时，错误消息消失了
        input_box = self.get_item_input_box()
        input_box.send_keys('a')
        time.sleep(1)
        self.assertFalse(
            self.get_error_element().is_displayed()
        )


    def test_003(self):
        ''' 新建清单时，提交空白文字会报错
            但是，我的清单能正常表示
        '''
        # 创建登录用户
        self.create_pre_authenticated_session('abc@163.com')
        self.browser.get(self.live_server_url)
        
        # 新建清单
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        # 我的清单列显示刚刚新建的清单(排在最前列)
        self.wait_for_row_in_my_lists_table(1, 'Reticulate splines')
        

        # --- 再新建一个待办事项清单 ---

        # 点击"待办事项"链接
        self.browser.find_element_by_link_text('应用').click()
        self.browser.find_element_by_link_text('待办事项').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('#id_jumbotron > h1').text,
            '新建待办事项'
        ))

        # 提交一个空格
        input_box = self.get_item_input_box()
        input_box.send_keys(' ')
        input_box.send_keys(Keys.ENTER)

        # 于是，得到一条错误消息
        self.assertEqual(
            self.get_error_element().text,
            '请输入内容！'
        )

        # 我的清单可以正常表示
        self.wait_for_row_in_my_lists_table(1, 'Reticulate splines')
