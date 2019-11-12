"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from bills import views


urlpatterns = [
    url(r'^index/$', views.index, name='bill_page'),
    url(r'^create$', views.create_bill, name='create_bill'),
    url(r'^(\d+)/$', views.view_bill_list, name='view_bill_list'),
    # url(r'^(\d+)/remove$', views.remove_list, name='remove_list'),
    # url(r'^(\d+)/remove_item$', views.remove_list_item, name='remove_list_item'),
]
