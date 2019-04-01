#!python
# coding: gbk
#------------------------------
# test_authentication.py
#------------------------------
# author: TangJianwei
# update: 2019-03-29
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token


User = get_user_model()


class AuthenticateTest(TestCase):
    
    def test_returns_None_if_no_such_token(self):
        login_user_object = PasswordlessAuthenticationBackend().authenticate(uid='abc123')
        self.assertIsNone(login_user_object)


    def test_returns_new_user_with_correct_email_if_token_exists(self):
        token_object = Token.objects.create(email='abc@163.com')
        login_user_object = PasswordlessAuthenticationBackend().authenticate(uid=token_object.uid)
        user_object = User.objects.get(email=token_object.email)
        self.assertEqual(login_user_object, user_object)


    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        token_object = Token.objects.create(email='abc@163.com')
        user_object = User.objects.create(email=token_object.email)
        login_user_object = PasswordlessAuthenticationBackend().authenticate(uid=token_object.uid)
        self.assertEqual(login_user_object, user_object)


class GetUserTest(TestCase):
    
    def test_gets_user_by_email(self):
        User.objects.create(email='other@163.com')
        user_object = User.objects.create(email='abc@163.com')
        self.assertEqual(
            user_object,
            PasswordlessAuthenticationBackend().get_user(email='abc@163.com')
        )


    def test_returns_None_if_no_user_with_that_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user(email='abc@163.com')
        )
