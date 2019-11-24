#------------------------------
# bills.tests.test_tags.test_view_billyms
#------------------------------
# Author: TangJianwei
# Create: 2019-11-24
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from bills.models import Billym, Bill
from bills.templatetags.bill_tags import view_billyms


class ViewBillymsTest(TestCase):

    def test_001(self):
        ''' 没有月账单数据
        '''
        # 其他用户的数据
        other_user = User.objects.create(email='other@163.com')
        Billym.objects.create(owner=other_user, year=2019, month=1)

        # 当前用户还没有月账单
        owner = User.objects.create(email='abc@163.com')
        self.assertEquals(len(Billym.objects.filter(owner=owner)), 0)

        # 没有指定被选中的月账单
        context = view_billyms(owner)
        self.assertEquals(len(context['billyms']), 0)
        self.assertIsNone(context['selected_billym'])


    def test_002(self):
        ''' 取得当前用户的月账单数据
        '''
        # 其他用户的数据
        other_user = User.objects.create(email='other@163.com')
        Billym.objects.create(owner=other_user, year=2019, month=1)

        # 当前用户的月账单
        owner = User.objects.create(email='abc@163.com')
        billym_1 = Billym.objects.create(owner=owner, year=2019, month=1)
        billym_2 = Billym.objects.create(owner=owner, year=2019, month=2)

        # 指定了被选中的月账单
        context = view_billyms(owner, billym_1)
        self.assertEquals(len(context['billyms']), 2)
        self.assertIn(billym_1, context['billyms'])
        self.assertIn(billym_2, context['billyms'])
        self.assertEquals(context['selected_billym'], billym_1)

