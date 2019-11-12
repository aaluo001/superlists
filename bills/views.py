#------------------------------
# bills.views
#------------------------------
# Author: TangJianwei
# Create: 2019-11-06
#------------------------------
from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Sum

from commons.views import get_owner
from bills.models import Billym, Bill
from bills.forms import BillForm

NOT_FOUND_BILLYM_ERROR = '没有找到该账单，或该账单已被删除！'


def get_billyms(request):
    owner = get_owner(request)
    if (not owner): return None
    else: return Billym.objects.filter(owner=owner)

def get_bills_on_today_created():
    return Bill.objects.filter(create_ts__date=timezone.now().date())


def index(request):
    context = {
        'form': BillForm(),
        'bills': get_bills_on_today_created(),
        'billyms': get_billyms(request),
    }
    return render(request, 'bills/index.html', context)


def create_bill(request):
    form = BillForm(data=request.POST)
    if (form.is_valid()):
        form.save(get_owner(request))
        return redirect(reverse('bill_page'))
    else:
        context = {
            'form': form,
            'bills': get_bills_on_today_created(),
            'billyms': get_billyms(request),
        }
        return render(request, 'bills/index.html', context)


def view_bill_list(request, billym_id):
    selected_billym = None
    try:
        selected_billym = Billym.objects.get(\
            owner=get_owner(request), id=billym_id)
    except Billym.DoseNotExist:
        messages.error(request, NOT_FOUND_BILLYM_ERROR)
        return redirect(reverse('bill_page'))

    bill_set = selected_billym.bill_set
    aggs = {}
    aggs.update(bill_set.filter(money__lt=0).aggregate(expends=Sum('money')))
    aggs.update(bill_set.filter(money__gt=0).aggregate(incomes=Sum('money')))
    aggs['balance'] = aggs['expends'] + aggs['incomes']

    context = {
        'selected_billym': selected_billym,
        'aggs': aggs,
        'bills': bill_set.all(),
        'billyms': get_billyms(request),
    }
    return render(request, 'bills/bill_list.html', context)
