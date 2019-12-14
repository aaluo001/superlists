#------------------------------
# commons.utils
#------------------------------
# Author: TangJianwei
# Create: 2019-11-28
#------------------------------
from datetime import datetime


def datetime_now():
    return datetime.now()

def datetime_to_str(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')

def to_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

def datetime_now_str():
    return datetime_to_str(datetime_now())


def date_now():
    return datetime.now().date()

def date_to_str(date):
    return date.strftime('%Y-%m-%d')

def to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')

def date_now_str():
    return date_to_str(date_now())

