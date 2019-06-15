#------------------------------
# functional_tests.test_layout_and_styling
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    ''' 画面布局与风格测试
    '''
    def test_001(self):
        ''' 输入框居中显示
            主要是检查Bootstrap是否加载
        '''
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        
        # 首页的输入框居中显示
        input_box = self.get_item_input_box()
        self.assertAlmostEqual( \
            input_box.location['x'] + input_box.size['width'] / 2, \
            512, \
            delta=10 \
        )
        self.add_list_item('testing')
        
        # 清单页面的输入框居中显示
        input_box = self.get_item_input_box()
        self.assertAlmostEqual( \
            input_box.location['x'] + input_box.size['width'] / 2, \
            512, \
            delta=10 \
        )

