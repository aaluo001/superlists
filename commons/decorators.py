#------------------------------
# commons.decorators
#------------------------------
# Author: TangJianwei
# Create: 2019-12-03
#------------------------------
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from .views import redirect_to_home_page


def require_login(func):
    def wrap(request, *args, **kwargs):
        if (request.user.is_authenticated):
            return func(request, *args, **kwargs)
        else:
            return redirect_to_home_page()
    return wrap


def require_ajax(func):
    def wrap(request, *args, **kwargs):
        if (not request.is_ajax()):
            return HttpResponseBadRequest()
        return func(request, *args, **kwargs)
    return wrap
