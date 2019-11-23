#------------------------------
# functional_tests.test_bills.test_bill_page
#------------------------------
# Author: TangJianwei
# Create: 2019-11-23
#------------------------------

from .base_bills import BillsTest

class BillPageTest(BillsTest):

    def test_001(self):
        ''' 未登录用户看不到 "应用" 菜单
        '''
        self.browser.get(self.live_server_url)

        # 主菜单栏
        navbar = self.browser.find_element_by_id('id_navigation')
        self.assertTrue(
            len(navbar.find_elements_by_link_text('Superlists')) > 0
        )

        # 未登录用户看不到 "应用" 菜单
        self.assertEquals(
            navbar.find_elements_by_link_text('应用'), []
        )
        # 未登录用户看不到 "账单" 菜单
        self.assertEquals(
            navbar.find_elements_by_link_text('账单'), []
        )

    def test_002(self):
        ''' 点击 "账单" 后，迁移到账单首页
        '''
        # 创建登录用户
        self.create_pre_authenticated_session('abc@163.com')

        self.browser.get(self.live_server_url)
        navbar = self.browser.find_element_by_id('id_navigation')
        navbar.find_element_by_link_text('应用').click()
        navbar.find_element_by_link_text('账单').click()

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('#id_jumbotron > h1').text,
            '新建账单'
        ))
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('#id_my_lists > .panel-heading > .panel-title').text,
            '我的账单'
        ))
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_view_billyms').text,
            '没有找到您的账单！'
        ))

        # 没有显示账单明细
        self.wait_for(lambda: self.assertEquals(
            self.browser.find_elements_by_id('id_bills_table'), []
        ))
