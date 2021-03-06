#------------------------------
# bills.tests.test_tags.test_view_billyms
#------------------------------
# Author: TangJianwei
# Create: 2019-11-24
#------------------------------
from decimal import Decimal
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
        self.assertEqual(len(context['bills']), 0)


    def test_002(self):
        ''' 只能取得当天的账单明细
        '''
        # 其他用户的数据
        self.make_other_data()

        # 当前用户的数据
        date = date_now()
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=date.year, month=date.month)

        # 以前的数据
        date_before = timezone.now() - timedelta(days=1)
        bill_before = Bill.objects.create(
            billym=billym, money=+32.1, date=date_before.date(), comment='date before'
        )
        bill_before.create_ts = date_before
        bill_before.save()

        # 当天的数据
        Bill.objects.create(billym=billym, money=1000.1, comment='todays bill 1', date=date)
        Bill.objects.create(billym=billym, money=-200.9, comment='todays bill 2', date=date)

        context = view_bills(owner)
        bills = context['bills']

        self.assertEqual(len(bills), 2)
        self.assertEqual(bills[0]['money'], Decimal('-200.9'))
        self.assertEqual(bills[0]['comment'], 'todays bill 2')
        self.assertEqual(bills[0]['date'], date)
        self.assertEqual(bills[1]['money'], Decimal('1000.1'))
        self.assertEqual(bills[1]['comment'], 'todays bill 1')
        self.assertEqual(bills[1]['date'], date)


    def test_011(self):
        ''' 被指定的月账单，没有账单明细
        '''
        # 其他用户的数据
        self.make_other_data()

        # 当前用户的数据
        date = date_now()
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=date.year, month=date.month)

        # 其他月份的月账单(不会被抽出)
        other_billym = Billym.objects.create(owner=owner, year=2019, month=1)
        Bill.objects.create(billym=other_billym, money='-99999.9', comment='other billym', date='2019-1-1')

        # 没有账单明细
        self.assertEqual(len(billym.bill_set.all()), 0)
        context = view_bills(owner, billym.id)
        self.assertEqual(len(context['bills']), 0)


    def test_012(self):
        ''' 被指定的月账单有账单明细
        '''
        # 其他用户的数据
        self.make_other_data()

        # 当前用户的数据
        date = date_now()
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=date.year, month=date.month)

        # 以前的数据
        date_before = timezone.now() - timedelta(days=1)
        bill_before = Bill.objects.create(
            billym=billym, money=+32.1, date=date_before.date(), comment='date before'
        )
        bill_before.create_ts = date_before
        bill_before.save()

        # 当天的数据
        Bill.objects.create(billym=billym, money=1000.1, comment='todays bill 1', date=date)
        Bill.objects.create(billym=billym, money=-200.9, comment='todays bill 2', date=date)

        # 其他月份的月账单(不会被抽出)
        other_billym = Billym.objects.create(owner=owner, year=2019, month=1)
        Bill.objects.create(billym=other_billym, money='-99999.9', comment='other billym', date='2019-1-1')

        context = view_bills(owner, billym.id)
        bills = context['bills']

        self.assertEqual(len(bills), 3)
        self.assertEqual(bills[0]['money'], Decimal('-200.9'))
        self.assertEqual(bills[0]['comment'], 'todays bill 2')
        self.assertEqual(bills[0]['date'], date)
        self.assertEqual(bills[1]['money'], Decimal('1000.1'))
        self.assertEqual(bills[1]['comment'], 'todays bill 1')
        self.assertEqual(bills[1]['date'], date)
        self.assertEqual(bills[2]['money'], Decimal('32.1'))
        self.assertEqual(bills[2]['comment'], 'date before')
        self.assertEqual(bills[2]['date'], date_before.date())
