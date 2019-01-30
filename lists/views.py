from django.shortcuts import render, redirect
from lists.models import Item


def homePage(vRequest):
    if (vRequest.method == 'POST'):
        Item.objects.create(text=vRequest.POST['item_text'])
        return redirect('/lists/the-only-list/')
    return render(vRequest, 'home.html')


def viewList(vRequest):
    vItems = Item.objects.all()
    vData = { \
        'items': vItems,
    }
    return render(vRequest, 'list.html', vData)

