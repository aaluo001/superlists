#------------------------------
# commons.views
#------------------------------
# Author: TangJianwei
# Create: 2019-11-06
#------------------------------
import json

from django.http import HttpResponse


def get_owner(request):
    if (request.user.is_authenticated): return request.user
    else: return None

def json_response(data):
    return HttpResponse(json.dumps(data), content_type='application/json')

