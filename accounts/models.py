#!python
# coding: gbk
#------------------------------
# accounts.models
#------------------------------
# Author: TangJianwei
# Create: 2019-03-26
#------------------------------
from django.db import models
from django.contrib import auth


auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class User(models.Model):
    email = models.EmailField(primary_key=True)
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    email = models.EmailField(primary_key=True)
    uid = models.CharField(max_length=40)

