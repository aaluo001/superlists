#------------------------------
# functional_tests.test_view_list
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ViewListTest(FunctionalTest):
    ''' 显示清单测试
    '''
    def test_001(self):
        ''' 通过URL显示清单
        '''
        # 新建清单
        self.browser.get(self.live_server_url)
        self.add_list_item('买一些孔雀羽毛')
        self.add_list_item('用孔雀羽毛做假蝇')

        # 取得当前URL，并关闭浏览器
        url = self.browser.current_url
        self.quit_browser()
        
        # 通过URL来显示清单
        self.init_browser()
        self.browser.get(url)
        
        # 发现之前输入的待办事项
        self.wait_for(lambda: self.assertIn(
            '买一些孔雀羽毛',
            self.browser.find_element_by_id('id_list_table').text
        ))
        
        self.wait_for(lambda: self.assertIn(
            '用孔雀羽毛做假蝇',
            self.browser.find_element_by_id('id_list_table').text
        ))

        