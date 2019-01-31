from django.shortcuts import render, redirect
from lists.models import Item
from lists.models import List


def homePage(vRequest):
    return render(vRequest, 'home.html')


def newList(vRequest):
    vList = List.objects.create()
    Item.objects.create( \
        text=vRequest.POST['item_text'], \
        list=vList \
    )
    return redirect('/lists/{}/'.format(vList.id))


def viewList(vRequest, vListId):
    vList  = List.objects.get(id=vListId)
    #vItems = Item.objects.filter(list=vList)
    vData  = { \
        #'items': vItems,
        'list': vList,
    }
    return render(vRequest, 'list.html', vData)


def addItem(vRequest, vListId):
    vList  = List.objects.get(id=vListId)
    Item.objects.create( \
        text=vRequest.POST['item_text'], \
        list=vList \
    )
    return redirect('/lists/{}/'.format(vList.id))

