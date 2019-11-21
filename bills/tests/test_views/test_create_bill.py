#------------------------------
# bills.tests.test_views.test_create_bill
#------------------------------
# Author: TangJianwei
# Create: 2019-11-17
#------------------------------
from datetime import datetime
from bs4 import BeautifulSoup

from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from bills.models import Billym, Bill
from bills.forms import BillForm


class CreateBillTest(TestCase):

    def post_create_bill(self, data):
        return self.client.post('/bills/create', data=data)

    def test_001(self):
        ''' 未登录用户会跳转到首页
        '''
        data = {
            'money': 10.1,
            'comment': 'this is a test.',
        }
        response = self.post_create_bill(data)
        self.assertRedirects(response, '/')


    def test_011(self):
        ''' 正常处理后，跳转到bills的index页面
        '''
        self.client.force_login(User.objects.create(email='abc@163.com'))
        data = {
            'money': 10.1,
            'comment': 'this is a test.',
        }
        response = self.post_create_bill(data)
        self.assertRedirects(response, '/bills/index/')

    def test_012(self):
        ''' 正常处理后，数据保存到数据库(一)
            新建一个账单，会产生一条billym和一条bill的数据
        '''
        user = User.objects.create(email='abc@163.com')
        self.client.force_login(user)
        data = {
            'money': 1234567.1,
            'comment': 'this is a test, 123456789012345.',
        }
        self.post_create_bill(data)

        billyms = Billym.objects.all()
        self.assertEquals(len(billyms), 1)

        billym = billyms[0]
        date = datetime.now().date()

        self.assertEquals(billym.owner, user)
        self.assertEquals(billym.year,  date.year)
        self.assertEquals(billym.month, date.month)

        bills = Bill.objects.all()
        self.assertEquals(len(bills), 1)

        bill = bills[0]
        self.assertEquals(bill.billym, billym)
        self.assertEquals(bill.money.to_eng_string(), '1234567.1')
        self.assertEquals(bill.comment, 'this is a test, 123456789012345.')
        self.assertEquals(bill.date, date)

    def test_013(self):
        ''' 正常处理后，数据保存到数据库(二)
            新建俩个以上的账单，会产生一条billym和多条bill的数据
            且多条bill的外键(billym)都是同一个billym
        '''
        user = User.objects.create(email='abc@163.com')
        self.client.force_login(user)
        data1 = {
            'money': -1234567.1,
            'comment': 'this is bill 1.',
        }
        data2 = {
            'money': -2.1,
            'comment': 'this is bill 2.',
        }
        data3 = {
            'money': 0,
            'comment': 'this is bill 3.',
        }
        self.post_create_bill(data1)
        self.post_create_bill(data2)
        self.post_create_bill(data3)

        billyms = Billym.objects.all()
        self.assertEquals(len(billyms), 1)

        bills = Bill.objects.all()
        self.assertEquals(len(bills), 3)

        for bill in bills:
            self.assertEquals(bill.billym, billyms[0])


    def test_021(self):
        ''' 提交出错时，数据不会保存到数据库
        '''
        user = User.objects.create(email='abc@163.com')
        self.client.force_login(user)
        data = {
            'money': 1.2,
            'comment': '',
        }
        self.post_create_bill(data)

        billyms = Billym.objects.all()
        bills = Bill.objects.all()
        self.assertEquals(len(billyms), 0)
        self.assertEquals(len(bills), 0)

    def test_022(self):
        ''' 提交出错时，迁移到index页面
            上下文中返回BillForm，且Form中的数据和输入的数据一样
        '''
        user = User.objects.create(email='abc@163.com')
        self.client.force_login(user)
        data = {
            'money': 1.22,
            'comment': 'this is the test.',
        }
        response = self.post_create_bill(data)
        form = response.context['form']

        # 迁移到index页面
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bills/index.html')

        # 上下文中返回BillForm
        self.assertIsInstance(form, BillForm)

        # Form中的数据和输入的数据一样
        soup = BeautifulSoup(form.as_p(), 'html.parser')
        text_money   = soup.find('input', {'name': 'money'})
        text_comment = soup.find('input', {'name': 'comment'})

        self.assertEquals(text_money['value'], '1.22')
        self.assertEquals(text_comment['value'], 'this is the test.')
