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
        date_before = timezone.now() - timedelta(days=1)
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=date_before.year, month=date_before.month)
        bill_before = Bill.objects.create(
            billym=billym, money=+32.1, date=date_before.date(), comment='date before 1'
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

        bill_1_fields = self.get_bill_record_fields(1)
        self.assertEquals(bill_1_fields[0].text, date_now_str())
        self.assertEquals(bill_1_fields[1].text, '-2000999.0')
        self.assertEquals(bill_1_fields[2].text, 'new bills 2')
        
        # 负数显示成红色
        self.assertEquals(
            bill_1_fields[1].find_element_by_css_selector('.text-danger').text,
            bill_1_fields[1].text
        )


        bill_2_fields = self.get_bill_record_fields(2)
        self.assertEquals(bill_2_fields[0].text, date_now_str())
        self.assertEquals(bill_2_fields[1].text, '1000999.0')
        self.assertEquals(bill_2_fields[2].text, 'new bills 1')
        
        # 正数不会显示成红色
        self.assertEquals(
            bill_2_fields[1].find_elements_by_css_selector('.text-danger'),
            []
        )


    def test_011(self):
        ''' 账单明细页面，不会显示其他用户的数据
        '''
        # 其他用户新建账单
        self.goto_bill_page('other_user@163.com')
        self.create_bill_normally('100.1', 'other users bills 1')
        self.create_bill_normally('-90.9', 'other users bills 2')
        self.quit_browser()

        # 当前用户访问浏览器
        self.init_browser()
        self.goto_bill_page('abc@163.com')
        self.create_bill_normally('-2000999', 'my bills')

        # 只能看到当前用户的账单明细
        self.select_billym()
        self.wait_for(lambda: self.assertEquals(
            len(self.get_bills()), 1
        ))
        bill_fields = self.get_bill_record_fields(1)
        self.assertEquals(bill_fields[0].text, date_now_str())
        self.assertEquals(bill_fields[1].text, '-2000999.0')
        self.assertEquals(bill_fields[2].text, 'my bills')

    def test_012(self):
        ''' 账单明细页面，可以显示当前用户以前的账单明细
        '''
        # 当前用户以前的数据
        date_before = timezone.now() - timedelta(days=1)
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=date_before.year, month=date_before.month)
        bill_before_1 = Bill.objects.create(
            billym=billym, money=-9991.1, date=date_before.date(), comment='date before 1'
        )
        bill_before_1.create_ts = date_before
        bill_before_1.save()

        bill_before_2 = Bill.objects.create(
            billym=billym, money=+32.1, date=date_before.date(), comment='date before 2'
        )
        bill_before_2.create_ts = date_before
        bill_before_2.save()


        # 当前用户访问浏览器
        self.goto_bill_page('abc@163.com')

        # 可以看到以前的账单明细
        self.select_billym()
        self.wait_for(lambda: self.assertEquals(
            len(self.get_bills()), 2
        ))

        bill_1_fields = self.get_bill_record_fields(1)
        self.assertEquals(bill_1_fields[0].text, date_before.date().strftime('%Y-%m-%d'))
        self.assertEquals(bill_1_fields[1].text, '32.1')
        self.assertEquals(bill_1_fields[2].text, 'date before 2')

        # 正数不会显示成红色
        self.assertEquals(
            bill_1_fields[1].find_elements_by_css_selector('.text-danger'),
            []
        )

        bill_2_fields = self.get_bill_record_fields(2)
        self.assertEquals(bill_2_fields[0].text, date_before.date().strftime('%Y-%m-%d'))
        self.assertEquals(bill_2_fields[1].text, '-9991.1')
        self.assertEquals(bill_2_fields[2].text, 'date before 1')
        
        # 负数显示成红色
        self.assertEquals(
            bill_2_fields[1].find_element_by_css_selector('.text-danger').text,
            bill_2_fields[1].text
        )

    def test_013(self):
        ''' 账单明细页面，不会显示其他未被选择的月账单数据
        '''
        # 其他月账单
        owner = User.objects.create(email='abc@163.com')
        billym_1 = Billym.objects.create(owner=owner, year=2019, month=10)
        Bill.objects.create(billym=billym_1, money=+912.9, comment='other billym 1', date='2019-10-01')
        billym_2 = Billym.objects.create(owner=owner, year=2019, month=11)
        Bill.objects.create(billym=billym_2, money=-499.0, comment='other billym 2', date='2019-11-11')

        # 当前用户访问浏览器
        self.goto_bill_page('abc@163.com')

        # 可以看到其他的月账单
        billym_elements = self.wait_for(lambda: self.get_billyms())
        self.assertEquals(len(billym_elements), 2)
        self.assertEquals(billym_elements[0].text, '2019年11月')
        self.assertEquals(billym_elements[1].text, '2019年10月')

        # 新建一条账单
        self.create_bill_normally('-2000999', 'my bills')

        # 可以看到刚刚新建的月账单
        billym_elements = self.wait_for(lambda: self.get_billyms())
        self.assertEquals(len(billym_elements), 3)
        self.assertEquals(billym_elements[0].text, '2019年12月')
        self.assertEquals(billym_elements[1].text, '2019年11月')
        self.assertEquals(billym_elements[2].text, '2019年10月')

        # 选择刚刚新建的月账单
        self.select_billym()
        self.wait_for(lambda: self.assertEquals(
            len(self.get_bills()), 1
        ))
        bill_fields = self.get_bill_record_fields(1)
        self.assertEquals(bill_fields[0].text, date_now_str())
        self.assertEquals(bill_fields[1].text, '-2000999.0')
        self.assertEquals(bill_fields[2].text, 'my bills')
