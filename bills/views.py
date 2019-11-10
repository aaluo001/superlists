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

from commons.views import get_owner
from bills.models import Billym, Bill
from bills.forms import BillForm


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

