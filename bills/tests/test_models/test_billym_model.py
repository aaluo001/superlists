#------------------------------
# bills.tests.test_models.test_billym_model
#------------------------------
# Author: TangJianwei
# Create: 2019-10-13
#------------------------------
from django.test import TestCase
from django.db.utils import IntegrityError
from django.db.transaction import TransactionManagementError
from django.contrib.auth import get_user_model
User = get_user_model()

from bills.models import Billym


class BillymModelTest(TestCase):
    ''' 月账单模型测试
    '''
    def test_001(self):
        ''' 字段测试：外键owner
        '''
        # 必须指定owner
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=2019, month=1)
        self.assertIn(billym, owner.billym_set.all())

        # 没有指定owner时会出错
        with self.assertRaises(IntegrityError):
            Billym.objects.create()


    def test_011(self):
        ''' 字段测试：year, month
            正常值设定
        '''
        owner = User.objects.create(email='abc@163.com')
        Billym.objects.create(owner=owner, year=2019, month=1)
        billyms = Billym.objects.all()
        self.assertEqual(billyms[0].year, 2019)
        self.assertEqual(billyms[0].month, 1)

    def test_012(self):
        ''' 字段测试：year
            异常值设定
        '''
        owner = User.objects.create(email='abc@163.com')

        # 必须指定
        with self.assertRaises(IntegrityError):
            Billym.objects.create(owner=owner, month=1)
        # 不能为空
        with self.assertRaises(ValueError):
            Billym.objects.create(owner=owner, year='', month=1)
        # 不能为字符串
        with self.assertRaises(TransactionManagementError):
            Billym.objects.create(owner=owner, year='2019', month=1)
        # 不能有小数
        with self.assertRaises(TransactionManagementError):
            Billym.objects.create(owner=owner, year=2019.3, month=1)

    def test_013(self):
        ''' 字段测试：month
            异常值设定
        '''
        owner = User.objects.create(email='abc@163.com')

        # 必须指定
        with self.assertRaises(IntegrityError):
            Billym.objects.create(owner=owner, year=2019)
        # 不能为空
        with self.assertRaises(ValueError):
            Billym.objects.create(owner=owner, year=2019, month='')
        # 不能为字符串
        with self.assertRaises(TransactionManagementError):
            Billym.objects.create(owner=owner, year=2019, month='1')
        # 不能有小数
        with self.assertRaises(TransactionManagementError):
            Billym.objects.create(owner=owner, year=2019, month=1.0)


    def test_021(self):
        ''' 同一拥有者不能重复登录同一年月
        '''
        owner = User.objects.create(email='abc@163.com')
        Billym.objects.create(owner=owner, year='2019', month=1)
        
        with self.assertRaises(IntegrityError):
            Billym.objects.create(owner=owner, year='2019', month=1)



    # def test_002(self):
    #     ''' 取得URL链接get_absolute_url()
    #     '''
    #     billym = List.objects.create()
    #     self.assertEqual( \
    #         Billym.get_absolute_url(), \
    #         '/lists/{}/'.format(Billym.id) \
    #     )




