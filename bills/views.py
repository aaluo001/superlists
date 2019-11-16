#------------------------------
# bills.views
#------------------------------
# Author: TangJianwei
# Create: 2019-11-06
#------------------------------
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
# from django.contrib import messages


from commons.views import get_owner
from bills.models import Billym, Bill
from bills.forms import BillForm


def index(request):
    context = {
        'form': BillForm(),
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
        }
        return render(request, 'bills/index.html', context)

def view_bill_list(request, billym_id):
    context = {
        'selected_billym_id': billym_id,
    }
    return render(request, 'bills/bill_list.html', context)
