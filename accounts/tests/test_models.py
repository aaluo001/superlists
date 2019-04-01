#!python
# coding: gbk
#------------------------------
# test_models.py
#------------------------------
# author: TangJianwei
# update: 2019-03-25
#------------------------------
from django.test import TestCase
from django.contrib import auth

from accounts.models import Token


User = auth.get_user_model()


class UserModelTest(TestCase):
    
    def test_user_is_valid_with_email_only(self):
        user_object = User(email='abc@163.com')
        user_object.full_clean()   # 不会出现异常

    def test_email_is_primary_key(self):
        user_object = User(email='abc@163.com')
        self.assertEqual(user_object.pk, 'abc@163.com')

    def test_no_problem_with_auth_login(self):
        user_object = User.objects.create(email='abc@163.com')
        user_object.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user_object) # 不会出现异常


class TokenModelTest(TestCase):
    
    def test_links_user_with_auto_generated_uid(self):
        token_object_1 = Token.objects.create(email='abc@163.com')
        token_object_2 = Token.objects.create(email='abc@163.com')
        self.assertNotEqual(token_object_1.uid, token_object_2.uid)

