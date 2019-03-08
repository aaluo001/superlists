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


def home_page(request):
    return render(request, 'home.html')


def new_list(request):
    list_object = List.objects.create()
    item_object = Item( \
        text=request.POST['item_text'], \
        list=list_object \
    )
    try:
        item_object.full_clean()
        item_object.save()
    except ValidationError as e:
        list_object.delete()
        return render(request, 'home.html', {'error': "您不能提交一个空的待办事项！"})
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

