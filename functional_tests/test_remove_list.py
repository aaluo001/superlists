#------------------------------
# functional_tests.test_remove_list
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class RemoveListTest(FunctionalTest):
    ''' 删除清单测试
    '''
    def test_001(self):
        ''' 删除清单后，跳转到"我的清单"页面
            且删除的清单无法访问
        '''
        # 创建登录用户
        self.create_pre_authenticated_session('abc@163.com')

        # 新建清单
        self.browser.get(self.live_server_url)
        self.add_list_item('买一些孔雀羽毛')
        self.add_list_item('用孔雀羽毛做假蝇')
        # 取得当前URL
        url = self.browser.current_url
        
        # 删除清单
        self.browser.find_element_by_css_selector('button#id_remove_list').click()

        # 迁移到"我的清单"页面
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('div.text-center > h1').text,
            '我的清单'
        ))
        self.assertIn('/lists/', self.browser.current_url)
        
        # 删除的清单无法访问
        self.browser.get(url)
        self.wait_for(lambda: self.assertIn(
            '没有找到该清单',
            self.browser.find_element_by_id('id_messages').text
        ))
        self.assertEqual(self.browser.current_url, self.live_server_url + '/')