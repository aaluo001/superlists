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
from bills.models import Billym, Bill
from bills.forms import BillForm


def get_billym_list(request):
    owner = get_owner(request)
    if (not owner): return None
    else: return Billym.objects.filter(owner=owner)


def index(request):
    context = {
        'form': BillForm(),
        'billym_list': get_billym_list(request),
    }
    return render(request, 'bills/index.html', context)


def create_bill(request):
    form = BillForm(data=request.POST)
    if (form.is_valid()):
        pass
    else:
        pass

    context = {
        'form': form,
        'billym_list': get_billym_list(request),
    }
    return render(request, 'bills/index.html', context)

