#!python
# coding: gbk
#------------------------------
# views.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from lists.models import Item
from lists.models import List
from lists.forms import ItemForm, ExistingListItemForm


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if (form.is_valid()):
        list_object = List.objects.create()
        form.save(for_list=list_object)
        return redirect(list_object)
    else:
        return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    list_object  = List.objects.get(id=list_id)
    form = None
    
    if (request.method == 'POST'):
        form = ExistingListItemForm(
            for_list=list_object, data=request.POST
        )
        if (form.is_valid()):
            form.save()
            return redirect(list_object)
    else:
        form = ExistingListItemForm(for_list=list_object)

    context = { \
        'list': list_object,
        'form': form,
    }
    return render(request, 'list.html', context)

