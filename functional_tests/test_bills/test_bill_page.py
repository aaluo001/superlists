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
        self.assertEqual(
            navbar.find_elements_by_link_text('应用'), []
        )
        # 未登录用户看不到 "账单" 菜单
        self.assertEqual(
            navbar.find_elements_by_link_text('账单'), []
        )


    def test_002(self):
        ''' 进入账单页面，查看标题和表单
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 标题
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('#id_jumbotron > h1').text,
            '新建账单'
        ))

        # 金额
        money_input_box = self.get_money_input_box()
        self.assertEqual(money_input_box.get_attribute('placeholder'), '正数为收入，负数为支出')
        self.assertEqual(money_input_box.get_attribute('class'), 'form-control')
        self.assertTrue(money_input_box.get_attribute('required'))

        # 备注
        comment_input_box = self.get_comment_input_box()
        self.assertEqual(comment_input_box.get_attribute('placeholder'), '收入支出说明')
        self.assertEqual(comment_input_box.get_attribute('maxlength'), '32')
        self.assertEqual(comment_input_box.get_attribute('class'), 'form-control')
        self.assertTrue(comment_input_box.get_attribute('required'))

        # 提交
        self.assertEqual(self.get_submit_button().text, '提交')
