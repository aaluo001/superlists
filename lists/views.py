from django.shortcuts import render


def homePage(vRequest):
    return render(vRequest, 'home.html')


