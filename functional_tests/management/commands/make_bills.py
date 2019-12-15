#------------------------------
# make_bills.py
#------------------------------
# author: TangJianwei
# update: 2019-04-14
#------------------------------
import pytz

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
User = get_user_model()

from commons.utils import to_datetime
from bills.models import Billym, Bill


def make_bills(email):
    owner = User.objects.create(email=email)

    billym_1 = Billym.objects.create(owner=owner, year=2018, month=12)
    bill = Bill.objects.create(billym=billym_1, money=-9991.1, date='2018-12-01', comment='billym_1: old bill 1')
    dt = to_datetime('2018-12-01 10:00:00')
    bill.create_ts = dt.replace(tzinfo=(pytz.timezone('Asia/Shanghai')))
    bill.save()
    bill = Bill.objects.create(billym=billym_1, money=+32.1, date='2018-12-11', comment='billym_1: old bill 2')
    dt = to_datetime('2018-12-11 10:23:00')
    bill.create_ts = dt.replace(tzinfo=(pytz.timezone('Asia/Shanghai')))
    bill.save()

    billym_2 = Billym.objects.create(owner=owner, year=2019, month=10)
    bill = Bill.objects.create(billym=billym_2, money=+912.9, date='2019-10-01', comment='billym_2: old bill 1')
    dt = to_datetime('2019-10-01 09:11:20')
    bill.create_ts = dt.replace(tzinfo=(pytz.timezone('Asia/Shanghai')))
    bill.save()

    billym_3 = Billym.objects.create(owner=owner, year=2019, month=11)
    bill = Bill.objects.create(billym=billym_3, money=-499.0, date='2019-11-11', comment='billym_3: old bill 1')
    dt = to_datetime('2019-11-11 12:00:01')
    bill.create_ts = dt.replace(tzinfo=(pytz.timezone('Asia/Shanghai')))
    bill.save()
    bill = Bill.objects.create(billym=billym_3, money=+599.1, date='2019-11-11', comment='billym_3: old bill 2')
    dt = to_datetime('2019-11-11 16:50:00')
    bill.create_ts = dt.replace(tzinfo=(pytz.timezone('Asia/Shanghai')))
    bill.save()


class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('email')

    def handle(self, *args, **kwargs):
        make_bills(kwargs['email'])
