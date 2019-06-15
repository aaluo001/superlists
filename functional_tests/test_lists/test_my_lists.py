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
        ''' 登录用户可以新建清单，然后在我的清单页面显示
        '''
        # 创建登录用户
        self.create_pre_authenticated_session('abc@163.com')
        
        # 新建清单
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        list_url_1 = self.browser.current_url

        # 点击"我的清单"链接
        self.browser.find_element_by_link_text('待办事项').click()
        self.browser.find_element_by_link_text('我的清单').click()

        # 巨幕显示"我的清单"
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('div.text-center > h1').text,
            '我的清单'
        ))

        # 我的清单页面出现新建的清单
        # 而清单名字是第一个待办事项的内容
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('ul#id_my_lists_table')
        )
        self.wait_for(lambda:
            self.browser.find_element_by_link_text('Reticulate splines')
        )

        # 进入清单页面，该页面的链接和新建清单的链接一致
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, list_url_1)
        )

        
        # --- 再新建一个待办事项清单 ---

        # 点击"新建清单"链接
        self.browser.find_element_by_link_text('待办事项').click()
        self.browser.find_element_by_link_text('新建清单').click()
        
        # 新建清单
        self.add_list_item('Click cows')
        list_url_2 = self.browser.current_url

        # 点击"我的清单"链接
        self.browser.find_element_by_link_text('待办事项').click()
        self.browser.find_element_by_link_text('我的清单').click()

        # 我的清单页面出现新建的清单
        # 而清单名字是第一个待办事项的内容
        self.wait_for(lambda:
            self.browser.find_element_by_link_text('Click cows')
        )
        
        # 进入清单页面，该页面的链接和新建清单的链接一致
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, list_url_2)
        )

        # 退出后"我的清单"链接不见了
        self.browser.find_element_by_link_text("退出").click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text("我的清单"),
            []
        ))

        
    def test_002(self):
        ''' 登录用户没有创建清单时，我的清单页面没有清单显示
        '''
        # 创建登录用户
        self.create_pre_authenticated_session('abc@163.com')
        self.browser.get(self.live_server_url)

        # 点击"我的清单"链接
        self.browser.find_element_by_link_text('待办事项').click()
        self.browser.find_element_by_link_text('我的清单').click()

        # 巨幕显示"我的清单"
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('div.text-center > h1').text,
            '我的清单'
        ))
        
        # 没有清单显示
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_css_selector('ul#id_my_lists_table'),
            []
        ))
        
        # 提示没有清单的消息
        self.wait_for(lambda: self.assertIn(
            '没有找到您的清单',
            self.browser.find_element_by_tag_name('body').text
        ))

    
    def test_003(self):
        ''' 匿名用户无法显示我的清单
        '''
        # 匿名用户新建清单
        self.browser.get(self.live_server_url)
        self.add_list_item('Work at office')
        self.add_list_item('Have a dinner')
        
        # 没有找到"待办事项"菜单
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('待办事项'),
            []
        ))

        # 使用URL地址强行进入"我的清单"
        self.browser.get(self.live_server_url + '/lists/')

        # 页面跳转到首页
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('div.text-center > h1').text,
            '新建清单'
        ))
        self.assertEqual(self.browser.current_url, self.live_server_url + '/')

