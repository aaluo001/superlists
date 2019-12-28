#------------------------------
# accounts.authentication
#------------------------------
# Author: TangJianwei
# Create: 2019-03-29
#------------------------------
from accounts.models import Token
from accounts.models import User


class PasswordlessAuthenticationBackend:
    
    def authenticate(self, request, uid):
        try:
            token_object = Token.objects.get(uid=uid)
            return User.objects.get(email=token_object.email)
        
        except Token.DoesNotExist:
            return None
        
        except User.DoesNotExist:
            return User.objects.create(email=token_object.email)


    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
