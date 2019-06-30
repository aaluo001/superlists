#------------------------------
# functional_tests.test_lists.test_remove_list
#------------------------------
# Author: TangJianwei
# Create: 2019-05-25
#------------------------------
import time

from selenium.webdriver.common.keys import Keys

from .base_lists import ListsTest


class RemoveListTest(ListsTest):
    ''' 删除清单测试
    '''
    def test_001(self):
        ''' 点击"删除清单"按钮后，弹出确认对话框(取消删除)
            选择Cancel按钮后，页面没有被提交
            该清单任然可以访问
        '''
        # 创建登录用户
        self.create_pre_authenticated_session('abc@163.com')

        # 新建清单
        self.browser.get(self.live_server_url)
        self.add_list_item('买一些孔雀羽毛')
        self.add_list_item('用孔雀羽毛做假蝇')
        # 取得当前URL
        url = self.browser.current_url
        
        # 点击"删除清单"按钮后，弹出确认对话框
        self.browser.find_element_by_css_selector('button[name="remove_list"]').click()
        self.wait_for(lambda: self.assertEqual(
            "待办事项清单被删除后将无法恢复！\n您确定要这么做吗？",
            self.browser.find_element_by_css_selector("#id_remove_list_dialog").text.strip(),
        ))

        # 选择Cancel按钮后，页面没有被提交
        self.browser.find_elements_by_css_selector("div.ui-dialog-buttonset > button")[1].click()
        time.sleep(5)
        self.assertEqual(url, self.browser.current_url)

        # 该清单任然可以访问
        self.browser.get(url)
        self.wait_for_row_in_list_table(1, '买一些孔雀羽毛')
        self.wait_for_row_in_list_table(2, '用孔雀羽毛做假蝇')


    def test_002(self):
        ''' 点击"删除清单"按钮后，弹出确认对话框(确定删除)
            选择OK按钮后，页面被提交，最后跳转到"我的清单"页面
            该清单无法访问
        '''
        # 创建登录用户
        self.create_pre_authenticated_session('abc@163.com')

        # 新建清单
        self.browser.get(self.live_server_url)
        self.add_list_item('买一些孔雀羽毛')
        self.add_list_item('用孔雀羽毛做假蝇')
        # 取得当前URL
        url = self.browser.current_url
        
        # 点击"删除清单"按钮后，弹出确认对话框
        self.browser.find_element_by_css_selector('button[name="remove_list"]').click()
        self.wait_for(lambda: self.assertEqual(
            "待办事项清单被删除后将无法恢复！\n您确定要这么做吗？",
            self.browser.find_element_by_css_selector("#id_remove_list_dialog").text.strip(),
        ))

        # 选择OK按钮后，页面被提交，最后跳转到"我的清单"页面
        self.browser.find_elements_by_css_selector("div.ui-dialog-buttonset > button")[0].click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('div.text-center > h1').text,
            '我的清单'
        ))
        self.assertIn('/lists/', self.browser.current_url)
        
        # 该清单无法访问(在首页显示提示消息)
        self.browser.get(url)
        self.wait_for(lambda: self.assertEqual(
            '没有找到该清单，或该清单已被删除！',
            self.browser.find_element_by_id('id_messages').text
        ))
        self.assertEqual(self.browser.current_url, self.live_server_url + '/')


    def test_003(self):
        ''' 匿名用户看不到"删除清单"按钮
        '''
        self.browser.get(self.live_server_url)
        self.add_list_item('New item')

        self.assertEqual(
            self.browser.find_elements_by_css_selector('button#id_remove_list'),
            []
        )

