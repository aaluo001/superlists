#------------------------------
# bills.tests.test_forms.test_bill_form
#------------------------------
# Author: TangJianwei
# Create: 2019-11-04
#------------------------------
from decimal import Decimal

from bs4 import BeautifulSoup
from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from bills.models import Billym, Bill
from bills.forms  import BillForm


class BillFormTest(TestCase):
    ''' 新建账单测试
    '''
    def test_001(self):
        ''' 新建账单输入框及其属性
        '''
        soup = BeautifulSoup(BillForm().as_p(), 'html.parser')
        # print(soup)
        text_money = soup.find('input', {'name': 'money'})
        self.assertEqual(text_money['type'], 'text')
        self.assertEqual(text_money['placeholder'], '正数为收入，负数为支出')
        self.assertEqual(text_money['required'], '')
        self.assertEqual(text_money['class'], ['form-control', ])

        text_comment = soup.find('input', {'name': 'comment'})
        self.assertEqual(text_comment['type'], 'text')
        self.assertEqual(text_comment['placeholder'], '收入支出说明')
        self.assertEqual(text_comment['maxlength'], '32')
        self.assertEqual(text_comment['required'], '')
        self.assertEqual(text_comment['class'], ['form-control', ])


    def test_011(self):
        ''' 字段测试：money
        '''
        form = BillForm(data={'money': '', 'comment': 'test', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['money'], ['请输入内容！', ])

        form = BillForm(data={'money': 'abc', 'comment': 'test', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['money'], ['请输入实数！', ])

        form = BillForm(data={'money': '12345678.1', 'comment': 'test', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['money'], ['请不要超过 8 个数字！', ])

        form = BillForm(data={'money': '9.11', 'comment': 'test', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['money'], ['请不要超过 1 位小数！', ])

        form = BillForm(data={'money': '12345678', 'comment': 'test', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['money'], ['请不要超过 7 位整数！', ])

        form = BillForm(data={'money': '-1234567.1', 'comment': 'test', })
        self.assertTrue(form.is_valid())

    def test_012(self):
        ''' 字段测试：comment
        '''
        form = BillForm(data={'money': '10.9', 'comment': '', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment'], ['请输入内容！', ])

        form = BillForm(
            data={
                'money': '10.9',
                'comment': '123456789012345678901234567890123',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment'], ['请不要超过 32 个字符！', ])

        form = BillForm(
            data={
                'money': '10.9',
                'comment': '这里一共有32个字符，234567890123456789012',
            }
        )
        self.assertTrue(form.is_valid())


    def test_021(self):
        ''' 将表单内容保存到数据库
        '''
        owner = User.objects.create(email='abc@163.com')

        # 确保当天新建的账单不会保存到other_billym
        other_billym = Billym.objects.create(owner=owner, year=2019, month=10)

        # 新建账单
        BillForm(
            data={
                'money': -9999999.9, 
                'comment':'最大长度测试：八九十一二三四五六七八九十一二三四五六七八九十！。',
            }
        ).save(owner=owner)
        BillForm(
            data={
                'money': +1234567.5, 
                'comment':'Inputs:89012345678901234567890!.',
            }
        ).save(owner=owner)
        
        billym = Billym.objects.first()
        bills = Bill.objects.all()
        self.assertEqual(len(bills), 2)
        self.assertEqual(bills[0].billym, billym)
        self.assertEqual(bills[1].billym, billym)
        self.assertNotEqual(billym, other_billym)

        self.assertEqual(bills[0].money, Decimal('1234567.5'))
        self.assertEqual(bills[0].comment, 'Inputs:89012345678901234567890!.')
        self.assertEqual(bills[0].date, datetime.now().date())

        self.assertEqual(bills[1].money, Decimal('-9999999.9'))
        self.assertEqual(bills[1].comment, '最大长度测试：八九十一二三四五六七八九十一二三四五六七八九十！。')
        self.assertEqual(bills[1].date, datetime.now().date())

