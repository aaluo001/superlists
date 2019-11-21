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
from django.conf.urls import url, include
from django.views.generic.base import RedirectView

from lists.views import home_page
from lists import urls as lists_urls
from accounts import urls as accounts_urls
from bills import urls as bills_urls
from bills import urls_api as bills_urls_api


urlpatterns = [
    url(r'^$', home_page, name='home_page'),
    url(r'^lists/', include(lists_urls)),
    url(r'^accounts/', include(accounts_urls)),
    url(r'^bills/', include(bills_urls, namespace='bills')),
    url(r'^api/bills/', include(bills_urls_api, namespace='api_bills')),
    url(r'^favicon.ico$', RedirectView.as_view(url='static/favicon.ico'))
]
