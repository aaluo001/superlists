#------------------------------
# bills.views_api
#------------------------------
# Author: TangJianwei
# Create: 2019-11-06
#------------------------------
from datetime import datetime
from django.db.models import Sum
from django.http import JsonResponse

from commons.views import get_owner
from bills.models import Billym, Bill


def bill_records(bills):
    return [
        {
            'money': bill.money.to_eng_string(),
            'comment': bill.comment,
            'date': datetime.strftime(bill.date, '%Y-%m-%d'),
        } for bill in bills
    ]

def get_billym(request, billym_id):
    ''' 取得指定的月账单
    '''
    owner = get_owner(request)
    if (not owner): return None
    else: return Billym.objects.get(owner=owner, id=billym_id)


def get_billyms(request):
    ''' 取得所有的月账单
    '''
    billyms = None
    owner = get_owner(request)
    if (not owner): return JsonResponse({'billyms': None})
    else: billyms = Billym.objects.filter(owner=owner)

    data = [
        {
            'id': billym.id,
            'year': billym.year,
            'month': billym.month,
            'url': billym.get_absolute_url()
        } for billym in billyms
    ]
    return JsonResponse({'billyms': data})

def get_bills_on_created_today(request):
    ''' 取得当天的账单明细
    '''
    bills = Bill.objects.filter(create_ts__date=datetime.now().date())
    return JsonResponse({'bills': bill_records(bills)})

def get_bills(request, billym_id):
    ''' 取得指定月账单的账单明细
    '''
    billym = get_billym(request, billym_id)
    if (not billym):
        return JsonResponse({'bills': None})
    else:
        return JsonResponse({'bills': bill_records(billym.bill_set.all())})

def get_aggregates_on_selected_billym(request, billym_id):
    ''' 统计指定的月账单
    '''
    billym = get_billym(request, billym_id)
    if (not billym): return JsonResponse({})

    expends = billym.bill_set.filter(money__lt=0).aggregate(expends=Sum('money'))['expends']
    incomes = billym.bill_set.filter(money__gt=0).aggregate(incomes=Sum('money'))['incomes']
    balance = expends + incomes

    data = {}
    data['year'] = billym.year
    data['month'] = billym.month
    data['expends'] = expends.to_eng_string()
    data['incomes'] = incomes.to_eng_string()
    data['balance'] = balance.to_eng_string()
    return JsonResponse(data)
