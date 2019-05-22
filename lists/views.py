#!python
# coding: gbk
#------------------------------
# lists.views
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import Item
from lists.models import List
from lists.forms import ItemForm, ExistingListItemForm


NOT_FOUND_LIST_ERROR = '没有找到该清单！'


def home_page(request):
    return render(request, 'lists/index.html', {'form': ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if (form.is_valid()):
        # 如果当前用户已经登录，就将当前用户绑定为清单的拥有者。
        # 不然清单将没有拥有者，可以被所有未登录用户查看。
        list_object = List()
        if (request.user.is_authenticated):
            list_object.owner = request.user
        list_object.save()

        form.save(for_list=list_object)
        return redirect(list_object)
    else:
        return render(request, 'lists/index.html', {'form': form})


def view_list(request, list_id):
    # 如果当前用户已经登录，那么只能看到自己的清单。
    # 不然只能看到没有绑定拥有者的清单。
    owner = None
    if (request.user.is_authenticated): owner = request.user

    list_object = None
    try:
        list_object = List.objects.get(id=list_id, owner=owner)
    except List.DoesNotExist:
        messages.error(request, NOT_FOUND_LIST_ERROR)
        return redirect(reverse('home_page'))


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
    return render(request, 'lists/list.html', context)


def remove_list(request, list_id):
    # 只有登录用户才能删除自己的清单。
    list_object = List.objects.get(id=list_id, owner=request.user)
    list_object.delete()
    return redirect(reverse('my_lists'))


def my_lists(request):
    # 只有登录用户才能查看自己的清单。
    return render(request, 'lists/my_lists.html')

