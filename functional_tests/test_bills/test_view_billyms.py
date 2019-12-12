#------------------------------
# functional_tests.test_bills.test_view_bills
#------------------------------
# Author: TangJianwei
# Create: 2019-12-8
#------------------------------
from django.contrib.auth import get_user_model
User = get_user_model()

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
        other_user = User.objects.create(email='other@163.com')
        Billym.objects.create(owner=other_user, year=2017, month=1)

        # 我的月账单
        owner = User.objects.create(email='abc@163.com')
        Billym.objects.create(owner=owner, year=2019, month=10)

        # 当前用户访问浏览器
        self.goto_bill_page('abc@163.com')
        billym_elements = self.wait_for(lambda: self.get_billyms())
        self.assertEqual(billym_elements[0].text, '2019年10月')
