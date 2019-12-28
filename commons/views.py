#------------------------------
# commons.views
#------------------------------
# Author: TangJianwei
# Create: 2019-11-06
#------------------------------
from django.shortcuts import redirect
from django.urls import reverse


def get_owner(request):
    if (request.user.is_authenticated): return request.user
    else: return None

def redirect_to_home_page():
    return redirect(reverse('home_page'))


