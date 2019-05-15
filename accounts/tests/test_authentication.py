#!python
# coding: gbk
#------------------------------
# accounts.tests.test_authentication
#------------------------------
# Author: TangJianwei
# Create: 2019-03-29
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token


class AuthenticateTest(TestCase):
    ''' 登录验证机能
    '''
    def test_returns_None_if_no_such_token(self):
        ''' 登录验证失败时，返回None
        '''
        login_user_object = PasswordlessAuthenticationBackend().authenticate(uid='abc123')
        self.assertIsNone(login_user_object)


    def test_returns_new_user_with_correct_email_if_token_exists(self):
        ''' 登录验证成功
            如果用户不存在，就返回新建用户
        '''
        token_object = Token.objects.create(email='abc@163.com')
        login_user_object = PasswordlessAuthenticationBackend().authenticate(uid=token_object.uid)
        user_object = User.objects.get(email=token_object.email)
        self.assertEqual(login_user_object, user_object)


    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        ''' 登录验证成功
            如果用户已经存在，就返回该用户
        '''
        token_object = Token.objects.create(email='abc@163.com')
        user_object = User.objects.create(email=token_object.email)
        login_user_object = PasswordlessAuthenticationBackend().authenticate(uid=token_object.uid)
        self.assertEqual(login_user_object, user_object)


class GetUserTest(TestCase):
    ''' 取得用户机能
    '''
    def test_gets_user_by_email(self):
        ''' 可以通过指定Email取得用户
        '''
        User.objects.create(email='other@163.com')
        user_object = User.objects.create(email='abc@163.com')
        self.assertEqual(
            user_object,
            PasswordlessAuthenticationBackend().get_user(email='abc@163.com')
        )


    def test_returns_None_if_no_user_with_that_email(self):
        ''' 指定Email的用户不存在时，返回None
        '''
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user(email='abc@163.com')
        )
