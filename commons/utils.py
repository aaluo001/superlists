#------------------------------
# commons.utils
#------------------------------
# Author: TangJianwei
# Create: 2019-11-28
#------------------------------
from datetime import datetime


def datetime_now():
    return datetime.now()

def datetime_now_str():
    return datetime_now().strftime('%Y-%m-%d %H:%M:%S')


def date_now():
    return datetime.now().date()

def date_now_str():
    return date_now().strftime('%Y-%m-%d')


