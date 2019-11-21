#------------------------------
# bills.views
#------------------------------
# Author: TangJianwei
# Create: 2019-11-06
#------------------------------
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
    if (not get_owner(request)): return redirect_to_home_page()
    return render(request, 'bills/bill_list.html', {'selected_billym_id': billym_id})
