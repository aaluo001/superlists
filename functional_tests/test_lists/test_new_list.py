#------------------------------
# functional_tests.test_lists.test_new_list
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from selenium.webdriver.common.keys import Keys

from .base_lists import ListsTest


class NewListTest(ListsTest):
    ''' 新建清单测试
    '''
    def test_001(self):
        ''' 新建清单
        '''
        # 访问应用首页
        # 可以看到页面标题，以及巨幕：新建清单
        self.browser.get(self.live_server_url)
        self.assertIn('Superlists', self.browser.title)
        self.assertIn('新建清单', self.browser.find_element_by_tag_name('h1').text)

        # 输入待办事项
        self.add_list_item('买一些孔雀羽毛')
        self.add_list_item('用孔雀羽毛做假蝇')


    def test_002(self):
        ''' 新建不同的清单
        '''
        # 新建第一个待办事项清单
        self.browser.get(self.live_server_url)
        self.add_list_item('买一些孔雀羽毛')
        list_url_1 = self.browser.current_url
        self.assertRegex(list_url_1, '/lists/.+/')
        
        # 关闭浏览器
        self.browser.quit()
        
        # 另启一个浏览器
        # 新建第二个待办事项清单
        self.init_browser()
        self.browser.get(self.live_server_url)
        self.add_list_item('买一盒牛奶')
        list_url_2 = self.browser.current_url
        self.assertRegex(list_url_2, '/lists/.+/')
        
        # 两个清单的URL是不一样的
        self.assertNotEqual(list_url_1, list_url_2)
        
        # 且不能看到第一个清单的内容
        # 只能看到自己清单的内容
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('买一些孔雀羽毛', page_text)
        self.assertIn('买一盒牛奶', page_text)

