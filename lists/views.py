#!python
# coding: gbk
#------------------------------
# views.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from django.shortcuts import render, redirect
from lists.models import Item
from lists.models import List


def home_page(request):
    return render(request, 'home.html')


def new_list(request):
    list_object = List.objects.create()
    Item.objects.create( \
        text=request.POST['item_text'], \
        list=list_object \
    )
    return redirect('/lists/{}/'.format(list_object.id))


def view_list(request, list_id):
    list_object  = List.objects.get(id=list_id)
    context = { \
        'list': list_object,
    }
    return render(request, 'list.html', context)


def add_item(request, list_id):
    list_object  = List.objects.get(id=list_id)
    Item.objects.create( \
        text=request.POST['item_text'], \
        list=list_object \
    )
    return redirect('/lists/{}/'.format(list_object.id))

