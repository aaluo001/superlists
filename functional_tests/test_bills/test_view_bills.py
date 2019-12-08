#------------------------------
# functional_tests.test_bills.test_view_bills
#------------------------------
# Author: TangJianwei
# Create: 2019-12-8
#------------------------------
from datetime import datetime
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

from commons.utils import date_now, date_now_str
from bills.models import Billym, Bill

from .base_bills import BillsTest


class ViewBillsTest(BillsTest):

    def test_001(self):
        ''' 新建账单页面，不会显示其他用户的数据
        '''
        # 其他用户新建账单
        self.goto_bill_page('other_user@163.com')
        self.create_bill_normally('100.1', 'other users bills 1')
        self.create_bill_normally('-90.9', 'other users bills 2')
        self.quit_browser()

        # 当前用户访问浏览器
        self.init_browser()
        self.goto_bill_page('abc@163.com')

        # 没有显示账单明细
        self.wait_for(lambda: self.assertEquals(
            self.get_bills(), []
        ))

    def test_002(self):
        ''' 新建账单页面，不会显示当前用户非当天的数据
        '''
        # 当前用户以前的数据
        owner = User.objects.create(email='abc@163.com')
        date = date_now()
        billym = Billym.objects.create(owner=owner, year=date.year, month=date.month)

        date_before = timezone.now() - timedelta(days=1)
        bill_before = Bill.objects.create(
            billym=billym, money=+32.1, date=date_before.date(), comment='date before'
        )
        bill_before.create_ts = date_before
        bill_before.save()

        # 当前用户访问浏览器
        self.goto_bill_page('abc@163.com')

        # 没有显示账单明细
        self.wait_for(lambda: self.assertEquals(
            self.get_bills(), []
        ))

    def test_003(self):
        ''' 新建账单页面，可以显示当前用户当天的数据
        '''
        # 新建一条账单
        self.goto_bill_page('abc@163.com')
        self.create_bill_normally('+1000999', 'new bills 1')
        self.create_bill_normally('-2000999', 'new bills 2')
        # 退出浏览器
        self.quit_browser()

        # 再次登录时，新建账单页面会显示当天的数据
        self.init_browser()
        self.goto_bill_page('abc@163.com')
        self.wait_for(lambda: self.assertEquals(
            len(self.get_bills()), 2
        ))

        bill_1 = self.browser.find_elements_by_css_selector('#id_bills_row_{} > td'.format(1))
        self.assertEquals(bill_1[0].text, date_now_str())
        self.assertEquals(bill_1[1].text, '-2000999.0')
        self.assertEquals(bill_1[2].text, 'new bills 2')

        bill_2 = self.browser.find_elements_by_css_selector('#id_bills_row_{} > td'.format(2))
        self.assertEquals(bill_2[0].text, date_now_str())
        self.assertEquals(bill_2[1].text, '1000999.0')
        self.assertEquals(bill_2[2].text, 'new bills 1')
