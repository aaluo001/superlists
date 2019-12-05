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
        ''' 进入账单页面，查看标题和我的账单
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

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

    def test_003(self):
        ''' 进入账单页面，查看表单
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 金额
        money_input_box = self.get_money_input_box()
        self.assertEquals(money_input_box.get_attribute('placeholder'), '正数为收入，负数为支出')
        self.assertEquals(money_input_box.get_attribute('class'), 'form-control')
        self.assertTrue(money_input_box.get_attribute('required'))

        # 备注
        comment_input_box = self.get_comment_input_box()
        self.assertEquals(comment_input_box.get_attribute('placeholder'), '收入支出说明')
        self.assertEquals(comment_input_box.get_attribute('maxlength'), '32')
        self.assertEquals(comment_input_box.get_attribute('class'), 'form-control')
        self.assertTrue(comment_input_box.get_attribute('required'))

        # 提交
        self.assertEquals(self.get_submit_button().text, '提交')
