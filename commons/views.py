#------------------------------
# commons.views
#------------------------------
# Author: TangJianwei
# Create: 2019-11-06
#------------------------------

def get_owner(request):
    if (request.user.is_authenticated): return request.user
    else: return None
