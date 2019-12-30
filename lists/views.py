#------------------------------
# lists.views
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST

from commons.decorators import require_login
from commons.views import get_owner
from commons.views import redirect_to_home_page

from lists.models import List, Item
from lists.forms import ItemForm, ExistingListItemForm


def home_page(request):
    return render(request, 'lists/index.html', {'form': ItemForm()})


@require_POST
def new_list(request):
    form = ItemForm(data=request.POST)
    if (form.is_valid()):
        # 如果当前用户已经登录，就将当前用户绑定为清单的拥有者。
        # 不然清单将没有拥有者，可以被所有未登录用户查看。
        list_object = List()
        list_object.owner = get_owner(request)
        list_object.save()
        form.save(for_list=list_object)
        return redirect(list_object)
    else:
        return render(request, 'lists/index.html', {'form': form})


def view_list(request, list_id):
    # 如果当前用户已经登录，那么只能看到自己的清单。
    # 不然只能看到没有绑定拥有者的清单。
    list_object = None
    try:
        list_object = List.objects.get(
            id=list_id, owner=get_owner(request)
        )
    except List.DoesNotExist:
        messages.error(request, '没有找到该清单，或该清单已被删除！')
        return redirect_to_home_page()


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
        'selected_list': list_object,
        'form': form,
    }
    return render(request, 'lists/list.html', context)


@require_login
def remove_list(request, list_id):
    try:
        list_object = List.objects.get(id=list_id, owner=request.user)
    except List.DoesNotExist:
        pass
    else:
        list_object.delete()
    return redirect_to_home_page()


@require_login
def remove_list_item(request, item_id):
    try:
        item_object = Item.objects.select_related('list').get(id=item_id, list__owner=request.user)
    except Item.DoesNotExist:
        return redirect_to_home_page()
    else:
        item_object.delete()
        if (item_object.list.item_set.count() == 0):
            item_object.list.delete()
            return redirect_to_home_page()
        else:
            return redirect(item_object.list)

    