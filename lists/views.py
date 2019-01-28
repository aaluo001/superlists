from django.shortcuts import render
#from django.http import HttpResponse


def homePage(vRequest):
    if (vRequest.method == 'POST'):
        return render(vRequest, 'home.html', \
            {'new_item_text': vRequest.POST['item_text']} \
        )
    return render(vRequest, 'home.html')


