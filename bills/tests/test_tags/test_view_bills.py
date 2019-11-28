#------------------------------
# bills.tests.test_tags.test_view_billyms
#------------------------------
# Author: TangJianwei
# Create: 2019-11-24
#------------------------------
from datetime import datetime
from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from commons.utils import date_now
from bills.models import Billym, Bill
from bills.templatetags.bill_tags import view_bills


class ViewBillsTest(TestCase):
    ''' 当天新建账单的账单明细
    '''
    def make_other_data(self):
        ''' 其他用户的数据
        '''
        date = date_now()
        other_user = User.objects.create(email='other@163.com')
        other_billym = Billym.objects.create(owner=other_user, year=date.year, month=date.month)
        Bill.objects.create(billym=other_billym, money=10, comment='other bill', date=date)


    def test_001(self):
        ''' 没有当天的账单明细
        '''
        # 其他用户的数据
        self.make_other_data()

        # 没有取得当前用户的账单明细
        owner = User.objects.create(email='abc@163.com')
        context = view_bills(owner)
        self.assertEquals(len(context['bills']), 0)


    def test_002(self):
        ''' 只能取得当天的账单明细
        '''
        # 其他用户的数据
        self.make_other_data()

        # 当前用户的数据
        date = date_now()
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=date.year, month=date.month)

        # 当天的数据
        Bill.objects.create(billym=billym, money=1000.1, comment='todays bill 1', date=date)
        Bill.objects.create(billym=billym, money=-200.9, comment='todays bill 2', date=date)

        # 以前的数据
        date_before = timezone.now() - timedelta(days=1)
        bill_before = Bill.objects.create(
            billym=billym, money=+32.1, date=date_before, comment='date before'
        )
        bill_before.create_ts = date_before
        bill_before.save()

        context = view_bills(owner)
        bills = context['bills']

        self.assertEquals(len(bills), 2)
        self.assertEquals(bills[0]['money'].to_eng_string(), '-200.9')
        self.assertEquals(bills[0]['comment'], 'todays bill 2')
        self.assertEquals(bills[0]['date'], date)
        self.assertEquals(bills[1]['money'].to_eng_string(), '1000.1')
        self.assertEquals(bills[1]['comment'], 'todays bill 1')
        self.assertEquals(bills[1]['date'], date)


    def test_011(self):
        ''' 被指定的月账单，没有账单明细
            不会取得其他月账单的账单明细
        '''
        self.fail('Finished the test!')


    def test_012(self):
        ''' 被指定的月账单有账单明细
            不会取得其他月账单的账单明细
        '''
        pass

