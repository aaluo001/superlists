#!python
# coding: gbk
#------------------------------
# lists.views.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import Item
from lists.models import List
from lists.forms import ItemForm, ExistingListItemForm


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if (form.is_valid()):
        # �����ǰ�û��Ѿ���¼���ͽ���ǰ�û���Ϊ�嵥��ӵ���ߡ�
        # ��Ȼ�嵥��û��ӵ���ߣ����Ա�����δ��¼�û��鿴��
        list_object = List()
        if (request.user.is_authenticated):
            list_object.owner = request.user
        list_object.save()

        form.save(for_list=list_object)
        return redirect(list_object)
    else:
        return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    # �����ǰ�û��Ѿ���¼����ôֻ�ܿ����Լ����嵥��
    # ��Ȼֻ�ܿ���û�а�ӵ���ߵ��嵥��
    owner = None
    if (request.user.is_authenticated): owner = request.user
    list_object = List.objects.get(id=list_id, owner=owner)
    
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


def remove_list(request, list_id):
    # ֻ�е�¼�û�����ɾ���Լ����嵥��
    list_object = List.objects.get(id=list_id, owner=request.user)
    list_object.delete()
    return redirect(reverse('my_lists'))


def my_lists(request):
    # ֻ�е�¼�û����ܲ鿴�Լ����嵥��
    return render(request, 'my_lists.html')

