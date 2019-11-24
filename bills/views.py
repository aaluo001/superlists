#------------------------------
# bills.views
#------------------------------
# Author: TangJianwei
# Create: 2019-11-06
#------------------------------
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from commons.views import get_owner
from commons.views import redirect_to_home_page
from bills.models import Billym, Bill
from bills.forms import BillForm


def index(request):
    # 只有登录用户才能使用该机能
    if (not get_owner(request)): return redirect_to_home_page()
    return render(request, 'bills/index.html', {'form': BillForm()})


def create_bill(request):
    # 只有登录用户才能使用该机能
    owner = get_owner(request)
    if (not owner): return redirect_to_home_page()

    form = BillForm(data=request.POST)
    if (form.is_valid()):
        form.save(owner)
        return redirect(reverse('bills:bill_page'))
    else:
        return render(request, 'bills/index.html', {'form': form})


def select_billym(request, billym_id):
    # 只有登录用户才能使用该机能
    owner = get_owner(request)
    if (not owner): return redirect_to_home_page()

    try:
        selected_billym = Billym.objects.get(owner=owner, id=billym_id)
    except Billym.DoesNotExist:
        messages.error(request, '没有找到该账单，或该账单已被删除！')
        return redirect(reverse('bills:bill_page'))
    else:
        expends = selected_billym.bill_set.filter(money__lt=0).aggregate(expends=Sum('money'))['expends']
        incomes = selected_billym.bill_set.filter(money__gt=0).aggregate(incomes=Sum('money'))['incomes']
        # 没有收入，或没有支出的处理
        if (expends is None): expends = 0
        if (incomes is None): incomes = 0

        context = {
            'selected_billym': selected_billym,
            'expends': expends,
            'incomes': incomes,
            'balance': expends + incomes,
        }
        return render(request, 'bills/selected_billym.html', context)
