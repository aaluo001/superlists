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
from django.views.decorators.http import require_POST

from commons.decorators import require_login
from bills.models import Billym, Bill
from bills.forms import BillForm


@require_login
def index(request):
    return render(request, 'bills/index.html', {'form': BillForm()})


@require_login
@require_POST
def create_bill(request):
    form = BillForm(data=request.POST)
    if (form.is_valid()):
        form.save(request.user)
        return redirect(reverse('bills:bill_page'))
    else:
        return render(request, 'bills/index.html', {'form': form})


@require_login
def select_billym(request, billym_id):
    try:
        selected_billym = Billym.objects.get(owner=request.user, id=billym_id)
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
