#------------------------------
# functional_tests.test_bills.test_view_bills
#------------------------------
# Author: TangJianwei
# Create: 2019-12-8
#------------------------------
from django.contrib.auth import get_user_model
User = get_user_model()

from functional_tests.management.commands.make_bills import make_bills
from functional_tests.server_tools import make_bills_on_server

from bills.models import Billym, Bill
from .base_bills import BillsTest


class ViewBillymsTest(BillsTest):

    def test_001(self):
        ''' 我的账单，查看标题
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 查看标题
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('#id_my_lists > .panel-heading > .panel-title').text,
            '我的账单'
        ))

    def test_002(self):
        ''' 我的账单，没有数据显示"没有找到您的账单"
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 没有数据显示"没有找到您的账单"
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_id('id_view_billyms').text,
            '没有找到您的账单！'
        ))

    def test_003(self):
        ''' 我的账单，只能看到当前用户的月账单
        '''
        # 其他用户新建账单
        self.goto_bill_page('other_user@163.com')
        self.create_bill_normally('100.1', 'other users bills 1')
        self.create_bill_normally('-90.9', 'other users bills 2')
        self.quit_browser()

        # 创建当前用户的账单明细
        if (self.staging_tests):
            make_bills_on_server('abc@163.com')
        else:
            make_bills('abc@163.com')

        # 当前用户访问浏览器
        self.init_browser()
        self.goto_bill_page('abc@163.com')

        # 可以看到所有的月账单
        billym_elements = self.wait_for(lambda: self.get_billyms())
        self.assertEqual(len(billym_elements), 3)
        self.assertEqual(billym_elements[0].text, '2019年11月')
        self.assertEqual(billym_elements[1].text, '2019年10月')
        self.assertEqual(billym_elements[2].text, '2018年12月')
