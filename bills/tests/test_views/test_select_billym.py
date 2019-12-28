#------------------------------
# bills.tests.test_views.test_select_billym
#------------------------------
# Author: TangJianwei
# Create: 2019-11-21
#------------------------------
from decimal import Decimal
from unittest.mock import patch, call

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

from bills.models import Billym, Bill


class SelectBillymTest(TestCase):

    def test_001(self):
        ''' 只有登录用户才是使用该机能，未登录用户会跳转到首页
        '''
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=2019, month=1)

        # 未登录用户会跳转到首页
        response = self.client.get(reverse('bills:select_billym', args=[billym.id,]))
        self.assertRedirects(response, '/')

        # 登录用户可以使用该机能，并迁移到selected_billym页面
        self.client.force_login(owner)
        response = self.client.get(reverse('bills:select_billym', args=[billym.id,]))
        self.assertTemplateUsed(response, 'bills/selected_billym.html')


    def test_002(self):
        ''' 上下文
        '''
        owner = User.objects.create(email='abc@163.com')
        self.client.force_login(owner)

        # 只有收入
        billym_1 = Billym.objects.create(owner=owner, year=2019, month=1)
        Bill.objects.create(billym=billym_1, money=10.9, comment='test 1', date='2019-01-01')
        Bill.objects.create(billym=billym_1, money=19.1, comment='test 2', date='2019-01-01')

        response = self.client.get(reverse('bills:select_billym', args=[billym_1.id,]))
        self.assertEqual(response.context['selected_billym'], billym_1)
        self.assertEqual(response.context['expends'], Decimal('0'))
        self.assertEqual(response.context['incomes'], Decimal('30'))
        self.assertEqual(response.context['balance'], Decimal('30'))


        # 只有支出
        billym_2 = Billym.objects.create(owner=owner, year=2019, month=2)
        Bill.objects.create(billym=billym_2, money=-1000000.3, comment='test 1', date='2019-02-21')

        response = self.client.get(reverse('bills:select_billym', args=[billym_2.id,]))
        self.assertEqual(response.context['selected_billym'], billym_2)
        self.assertEqual(response.context['expends'], Decimal('-1000000.3'))
        self.assertEqual(response.context['incomes'], Decimal('0'))
        self.assertEqual(response.context['balance'], Decimal('-1000000.3'))


        # 收入和支出同时存在
        billym_3 = Billym.objects.create(owner=owner, year=2019, month=3)
        Bill.objects.create(billym=billym_3, money=9999999.9, comment='test 1', date='2019-03-01')
        Bill.objects.create(billym=billym_3, money=1000.1, comment='test 2', date='2019-03-01')
        Bill.objects.create(billym=billym_3, money=-9999999.9, comment='test 3', date='2019-03-01')
        Bill.objects.create(billym=billym_3, money=-0.1, comment='test 4', date='2019-03-01')

        response = self.client.get(reverse('bills:select_billym', args=[billym_3.id,]))
        self.assertEqual(response.context['selected_billym'], billym_3)
        self.assertEqual(response.context['expends'], Decimal('-10000000'))
        self.assertEqual(response.context['incomes'], Decimal('10001000'))
        self.assertEqual(response.context['balance'], Decimal('1000.0'))


    @patch('bills.views.messages')
    def test_003(self, mock_messages):
        ''' 访问一个不存在的月账单
            跳转到新建账单页面，并显示提示消息。
        '''
        owner = User.objects.create(email='abc@163.com')
        self.client.force_login(owner)

        # 没有月账单的数据
        self.assertEqual(len(Billym.objects.all()), 0)
        # 访问一个不存在的月账单
        response = self.client.get(reverse('bills:select_billym', args=[1,]))
        
        # 跳转到新建账单页面
        self.assertRedirects(response, reverse('bills:bill_page'))
        self.assertEqual(
            mock_messages.error.call_args,
            call(response.wsgi_request, '没有找到该账单，或该账单已被删除！')
        )


    @patch('bills.views.messages')
    def test_004(self, mock_messages):
        ''' 访问别人的月账单
            跳转到新建账单页面，并显示提示消息。
        '''
        other_user = User.objects.create(email='other@163.com')
        billym = Billym.objects.create(owner=other_user, year=2019, month=1)

        owner = User.objects.create(email='abc@163.com')
        self.client.force_login(owner)

        # 访问别人的月账单
        response = self.client.get(reverse('bills:select_billym', args=[billym.id,]))

        # 跳转到新建账单页面
        self.assertRedirects(response, reverse('bills:bill_page'))
        self.assertEqual(
            mock_messages.error.call_args,
            call(response.wsgi_request, '没有找到该账单，或该账单已被删除！')
        )

