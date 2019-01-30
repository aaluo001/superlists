from django.shortcuts import render, redirect
from lists.models import Item
from lists.models import List


def homePage(vRequest):
    return render(vRequest, 'home.html')


def newList(vRequest):
    Item.objects.create( \
        text=vRequest.POST['item_text'], \
        list=List.objects.create() \
    )
    return redirect('/lists/the-only-list/')


def viewList(vRequest):
    vItems = Item.objects.all()
    vData = { \
        'items': vItems,
    }
    return render(vRequest, 'list.html', vData)

