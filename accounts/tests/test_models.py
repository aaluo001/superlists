#!python
# coding: gbk
#------------------------------
# accounts.tests.test_models
#------------------------------
# Author: TangJianwei
# Create: 2019-03-25
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model, login
User = get_user_model()

from accounts.models import Token


class UserModelTest(TestCase):
    ''' 测试用户模型
    '''
    def test_user_is_valid_with_email_only(self):
        ''' 确保用户可以正常使用，如果只设置Email的话
        '''
        user_object = User(email='abc@163.com')
        user_object.full_clean()   # 不会出现异常


    def test_email_is_primary_key(self):
        ''' 确保用户模型的PrimaryKey是Email
        '''
        user_object = User(email='abc@163.com')
        self.assertEqual(user_object.pk, 'abc@163.com')


    def test_no_problem_with_auth_login(self):
        ''' 确保使用Django提供的login机能可以正常使用
        '''
        user_object = User.objects.create(email='abc@163.com')
        user_object.backend = ''
        request = self.client.request().wsgi_request
        login(request, user_object) # 不会出现异常


class TokenModelTest(TestCase):
    ''' 测试登录验证模型
    '''
    def test_email_is_primary_key(self):
        ''' 确保登录验证模型的PrimaryKey是Email
        '''
        token_object = Token(email='abc@163.com')
        self.assertEqual(token_object.pk, 'abc@163.com')

