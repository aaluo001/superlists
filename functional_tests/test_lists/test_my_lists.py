#------------------------------
# functional_tests.test_lists.test_my_lists
#------------------------------
# Author: TangJianwei
# Create: 2019-04-04
#------------------------------
import time

from .base_lists import ListsTest


class MyListsTest(ListsTest):
    ''' 我的清单测试
    '''
    def test_001(self):
        ''' 登录用户没有创建任何清单时，我的清单列表显示没有清单
        '''
        # 创建登录用户
        self.create_pre_authenticated_session('abc@163.com')
        
        # 访问首页
        # 巨幕显示"新建待办事项"，在"我的待办事项"列显示"没有找到您的待办事项！"
        self.browser.get(self.live_server_url)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('#id_jumbotron > h1').text,
            '新建待办事项'
        ))
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('#id_my_lists > .panel-heading > .panel-title').text,
            '我的待办事项'
        ))
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('#id_my_lists > .panel-body > p').text,
            '没有找到您的待办事项！'
        ))


    def test_002(self):
        ''' 登录用户可以新建清单，然后在我的清单列显示
            退出登录后，将不再显示我的清单
        '''
        # 创建登录用户
        self.create_pre_authenticated_session('abc@163.com')
        self.browser.get(self.live_server_url)

        # 新建清单
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        list_url_1 = self.browser.current_url

        # 我的清单列显示刚刚新建的清单(排在最前列)
        # 且清单名字是第一个待办事项的内容(被选中状态)
        self.wait_for_row_in_my_lists_table(1, 'Reticulate splines')
        self.wait_for_selected_item_in_my_lists('Reticulate splines')

        # 进入清单页面，该页面的链接和新建清单的链接一致
        self.click_item_in_my_lists('Reticulate splines')
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, list_url_1)
        )

        
        # --- 再新建一个待办事项清单 ---

        # 点击"待办事项"链接
        self.browser.find_element_by_link_text('应用').click()
        self.browser.find_element_by_link_text('待办事项').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('#id_jumbotron > h1').text,
            '新建待办事项'
        ))

        # 新建清单
        self.add_list_item('Click cows')
        list_url_2 = self.browser.current_url

        # 我的清单列显示刚刚新建的清单(排在最前列)
        # 且清单名字是第一个待办事项的内容(被选中状态)
        self.wait_for_row_in_my_lists_table(1, 'Click cows')
        self.wait_for_selected_item_in_my_lists('Click cows')

        # 刚刚新建的清单被排在第二列
        self.wait_for_row_in_my_lists_table(2, 'Reticulate splines')


        # 进入清单页面，该页面的链接和新建清单的链接一致
        self.click_item_in_my_lists('Click cows')
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, list_url_2)
        )
        self.click_item_in_my_lists('Reticulate splines')
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, list_url_1)
        )

        # 退出后，返回"新建待办事项"页面
        self.browser.find_element_by_link_text("退出").click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('#id_jumbotron > h1').text,
            '新建待办事项'
        ))

        # "我的待办事项"列不再显示任何清单内容(显示未登录信息)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('div#id_my_lists > div.panel-body > p').text,
            '您还没有登录！'
        ))
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_css_selector("#id_my_lists_table"),
            []
        ))

    
    def test_003(self):
        ''' 匿名用户无法显示我的清单
        '''
        # 匿名用户新建清单
        self.browser.get(self.live_server_url)
        self.add_list_item('Work at office')
        self.add_list_item('Have a dinner')
        
        # "我的清单"列不再显示任何清单内容(显示未登录信息)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('div#id_my_lists > div.panel-body > p').text,
            '您还没有登录！'
        ))
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_css_selector("#id_my_lists_table"),
            []
        ))
