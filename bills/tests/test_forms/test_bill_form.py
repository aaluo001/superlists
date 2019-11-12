#------------------------------
# bills.tests.test_forms.test_bill_form
#------------------------------
# Author: TangJianwei
# Create: 2019-11-04
#------------------------------
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
        money_text = soup.find('input', {'name': 'money'})
        self.assertEqual(money_text['type'], 'text')
        self.assertEqual(money_text['placeholder'], '正数为收入，负数为支出')
        self.assertEqual(money_text['required'], '')
        self.assertEqual(money_text['class'], ['form-control', ])

        comment_text = soup.find('input', {'name': 'comment'})
        self.assertEqual(comment_text['type'], 'text')
        self.assertEqual(comment_text['placeholder'], '收入支出说明')
        self.assertEqual(comment_text['maxlength'], '32')
        self.assertEqual(comment_text['required'], '')
        self.assertEqual(comment_text['class'], ['form-control', ])


    def test_011(self):
        ''' 字段测试：money
        '''
        form = BillForm(data={'money': '', 'comment': 'test', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['money'], ['收入支出：不能为空！', ])

        form = BillForm(data={'money': 'abc', 'comment': 'test', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['money'], ['收入支出：请输入实数！', ])

        form = BillForm(data={'money': '12345678.1', 'comment': 'test', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['money'], ['收入支出：不能超过 8 个数字！', ])

        form = BillForm(data={'money': '9.11', 'comment': 'test', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['money'], ['收入支出：不能超过 1 位小数！', ])

        form = BillForm(data={'money': '12345678', 'comment': 'test', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['money'], ['收入支出：不能超过 7 位整数！', ])

        form = BillForm(data={'money': '-1234567.1', 'comment': 'test', })
        self.assertTrue(form.is_valid())

    def test_012(self):
        ''' 字段测试：comment
        '''
        form = BillForm(data={'money': '10.9', 'comment': '', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment'], ['备注：不能为空！', ])

        form = BillForm(
            data={
                'money': '10.9',
                'comment': '123456789012345678901234567890123',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment'], ['备注：不能超过 32 个字符！', ])

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
        BillForm(data={'money': -10.9, 'comment':'Buy a cup of tea.'}).save(owner=owner)
        BillForm(data={'money': +20.5, 'comment':'Inputs.'}).save(owner=owner)
        
        billym = Billym.objects.first()
        bills = Bill.objects.all()
        self.assertEqual(len(bills), 2)
        self.assertEqual(bills[0].billym, billym)
        self.assertEqual(bills[1].billym, billym)
        self.assertNotEqual(billym, other_billym)

        self.assertEqual(bills[0].money.to_eng_string(), '20.5')
        self.assertEqual(bills[0].comment, 'Inputs.')
        self.assertEqual(bills[0].date, datetime.now().date())

        self.assertEqual(bills[1].money.to_eng_string(), '-10.9')
        self.assertEqual(bills[1].comment, 'Buy a cup of tea.')
        self.assertEqual(bills[1].date, datetime.now().date())

