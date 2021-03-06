#------------------------------
# bills.tests.test_models.test_bill_model
#------------------------------
# Author: TangJianwei
# Create: 2019-10-13
#------------------------------
from decimal import Decimal
from decimal import InvalidOperation

from datetime import datetime
from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.db.utils import IntegrityError
from django.db.transaction import TransactionManagementError
from django.db.models import Count
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

from bills.models import Billym, Bill


class BillModelTest(TestCase):
    ''' 日账单模型测试
    '''
    def test_001(self):
        ''' 外键测试：billym
        '''
        # 必须指定billym
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=2019, month=1)

        bill1 = Bill.objects.create(billym=billym, money=10.1, date='2019-1-1', comment='input1')
        bill2 = Bill.objects.create(billym=billym, money=10.5, date='2019-1-1', comment='input2')
        self.assertIn(bill1, billym.bill_set.all())
        self.assertIn(bill2, billym.bill_set.all())

        # 没有指定owner时会出错
        with self.assertRaises(IntegrityError):
            Bill.objects.create(billym=None)


    def test_011(self):
        ''' 字段测试：money, date, comment
            正常值设定
        '''
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=2019, month=1)

        Bill.objects.create(billym=billym, money=10.5, date='2019-1-1', comment='input')
        bills = Bill.objects.all()
        self.assertEqual(bills[0].money, 10.5)
        self.assertEqual(bills[0].date, datetime(2019, 1, 1).date())
        self.assertEqual(bills[0].comment, 'input')

        #time_delay = datetime.now() - bills[0].create_ts.replace(tzinfo=None)
        #print(time_delay)
        self.assertAlmostEqual(
            bills[0].create_ts.replace(tzinfo=None), 
            datetime.now(), 
            delta=timedelta(hours=8, seconds=1)
        )
        # PS:
        # 数据库中取得create_ts的时区tzinfo是UTC时区，
        # 而datetime.now()没有指定时区，即时区是None，
        # 那么在比较时，必须统一时区，不然会出错。
        # 这里把数据库取得create_ts的时区设为None，
        # 比较结果是，create_ts与当前datetime.now()相差8小时。

        # 如果使用django自带的timezone.now()，就可以解决上面的问题
        self.assertAlmostEqual(
            bills[0].create_ts,
            timezone.now(),
            delta=timedelta(seconds=1)
        )


    def test_012(self):
        ''' 字段测试：money
            异常值设定
        '''
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=2019, month=1)

        # 必须指定
        with self.assertRaises(IntegrityError):
            Bill.objects.create(billym=billym, date='2019-1-1', comment='input')
        # 不能为空
        with self.assertRaises(ValidationError):
            Bill.objects.create(billym=billym, money='', date='2019-1-1', comment='input')
        # 不能为字符串
        with self.assertRaises(TransactionManagementError):
            Bill.objects.create(billym=billym, money='10.2', date='2019-1-1', comment='input')
        # 不能有超过1位小数
        with self.assertRaises(TransactionManagementError):
            Bill.objects.create(billym=billym, money=10.12, date='2019-1-1', comment='input')
        # 不能有超过8位整数
        with self.assertRaises(InvalidOperation):
            Bill.objects.create(billym=billym, money=123456789.1, date='2019-1-1', comment='input')

    def test_013(self):
        ''' 字段测试：date
            异常值设定
        '''
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=2019, month=1)

        # 必须指定
        with self.assertRaises(IntegrityError):
            Bill.objects.create(billym=billym, money=10.1, comment='input')
        # 不能为空
        with self.assertRaises(ValidationError):
            Bill.objects.create(billym=billym, money=10.1, date='', comment='input')
        # 不能为字符串
        with self.assertRaises(ValidationError):
            Bill.objects.create(billym=billym, money=10.1, date='1', comment='input')
        # 不能有小数
        with self.assertRaises(TypeError):
            Bill.objects.create(billym=billym, money=10.1, date=1.1, comment='input')

    def test_014(self):
        ''' 字段测试：comment
            异常值设定
        '''
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=2019, month=1)

        # 必须指定
        with self.assertRaises(IntegrityError):
            Bill.objects.create(billym=billym, money=10.1, date='2019-1-1', comment=None)
        # PS:
        # 如果没有指定comment, 就像这样
        #   bill = Bill.objects.create(billym=billym, money=10.1, date=1)
        # 程序也不会出错，那么，默认的comment会是什么呢？
        # 执行 print(bill.comment)，会发现程序执行到这里换行了。
        # 所以，默认的comment可能是换行符。

        # 不能为空
        with self.assertRaises(TransactionManagementError):
            Bill.objects.create(billym=billym, money=10.1, date='2019-1-1', comment='')
        # 不能为数值
        with self.assertRaises(TransactionManagementError):
            Bill.objects.create(billym=billym, money=10.1, date='2019-1-1', comment=1.0)


    def make_other_data(self):
        ''' 生成其他用户的数据
        '''
        other_user = User.objects.create(email='other@163.com')
        billym_1 = Billym.objects.create(owner=other_user, year=2019, month=1)
        billym_2 = Billym.objects.create(owner=other_user, year=2019, month=2)

        Bill.objects.create(billym=billym_1, money=-12.2, date='2019-01-01', comment='other_user-1')
        Bill.objects.create(billym=billym_1, money=-18.5, date='2019-01-02', comment='other_user-2')
        Bill.objects.create(billym=billym_1, money=+20.0, date='2019-01-16', comment='other_user-3')
        Bill.objects.create(billym=billym_2, money=-12.9, date='2019-02-01', comment='other_user-4')
        Bill.objects.create(billym=billym_2, money=+11.8, date='2019-03-29', comment='other_user-5')

    def make_data(self):
        ''' 生成当前用户的数据
        '''
        owner = User.objects.create(email='abc@163.com')
        billym_1 = Billym.objects.create(owner=owner, year=2019, month=1)
        billym_2 = Billym.objects.create(owner=owner, year=2019, month=2)

        # 当天的数据
        Bill.objects.create(billym=billym_1, money=-10.1, date='2019-01-01', comment='2019-01-01 billym-1')
        Bill.objects.create(billym=billym_1, money=-12.5, date='2019-01-05', comment='2019-01-05 billym-1')
        Bill.objects.create(billym=billym_1, money=-10.0, date='2019-01-19', comment='2019-01-19 billym-1')
        Bill.objects.create(billym=billym_2, money=-10.9, date='2019-02-10', comment='2019-02-10 billym-2')
        Bill.objects.create(billym=billym_2, money=+19.8, date='2019-02-21', comment='2019-02-21 billym-2')

        # 以前的数据
        bill_before_1 = Bill.objects.create(
            billym=billym_1, money=+32.1, date='2019-01-22', comment='2019-01-22 billym-before-1'
        )
        bill_before_1.create_ts = timezone.now() - timedelta(days=1)
        bill_before_1.save()
        bill_before_2 = Bill.objects.create(
            billym=billym_2, money=+29.8, date='2019-01-26', comment='2019-01-26 billym-before-2'
        )
        bill_before_2.create_ts = timezone.now() - timedelta(days=4)
        bill_before_2.save()


    def test_021(self):
        ''' 取得当天的数据，并降序排列
        '''
        self.make_other_data()
        self.make_data()

        # 结合月账单信息联合查询
        # 取得当天的数据，并降序排列
        owner = User.objects.get(email='abc@163.com')
        bills = Bill.objects.select_related('billym')\
            .filter(billym__owner=owner)\
            .filter(create_ts__date=timezone.now().date()).order_by('-id')

        # 打印出SQL语句
        # print(bills.query)

        # print(type(bills[0].money))
        # 这是<class 'decimal.Decimal'>类型，即Decimal('19.8')
        # 通过to_eng_string()来取得其字符串。

        self.assertEqual(len(bills), 5)

        self.assertEqual(bills[0].date, datetime(2019, 2, 21).date())
        self.assertEqual(bills[0].money, Decimal('19.8'))
        self.assertEqual(bills[0].billym.year, 2019)
        self.assertEqual(bills[0].billym.month, 2)

        self.assertEqual(bills[3].date, datetime(2019, 1, 5).date())
        self.assertEqual(bills[3].money, Decimal('-12.5'))
        self.assertEqual(bills[3].billym.year, 2019)
        self.assertEqual(bills[3].billym.month, 1)

    def test_022(self):
        ''' 统计月份账单的件数，及合计收入支出
        '''
        self.make_other_data()
        self.make_data()

        # 统计月份账单的件数，及合计收入支出
        owner = User.objects.get(email='abc@163.com')        
        billyms = Billym.objects.filter(owner=owner)\
            .annotate(bills_count=Count('bill'), bills_sum=Sum('bill__money'))
        
        # 打印出SQL语句
        #print(billyms.query)

        self.assertEqual(len(billyms), 2)
        self.assertEqual(billyms[0].year, 2019)
        self.assertEqual(billyms[0].month, 2)
        self.assertEqual(billyms[0].bills_count, 3)
        self.assertEqual(billyms[0].bills_sum, Decimal('38.7'))
        self.assertEqual(billyms[1].bills_count, 4)
        self.assertEqual(billyms[1].bills_sum, Decimal('-0.5'))

    def test_023(self):
        ''' 统计月份账单的收入与支出
        '''
        self.make_other_data()
        self.make_data()

        owner = User.objects.get(email='abc@163.com')        
        billyms = Billym.objects.filter(owner=owner)

        bills_1 = Bill.objects.filter(billym=billyms[0])
        incomes = bills_1.filter(money__gt=0).aggregate(incomes=Sum('money'))['incomes']
        expends = bills_1.filter(money__lt=0).aggregate(expends=Sum('money'))['expends']

        self.assertEqual(incomes, Decimal('49.6'))
        self.assertEqual(expends, Decimal('-10.9'))
        self.assertEqual((incomes + expends), Decimal('38.7'))
