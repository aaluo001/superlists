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
    ''' 用户模型
    '''
    def test_user_is_valid_with_email_only(self):
        ''' 用户模型可以正常使用，如果只设置Email字段
        '''
        user_object = User(email='abc@163.com')
        user_object.full_clean()        ## 这里不会出现异常


    def test_email_is_primary_key(self):
        ''' 用户模型的PrimaryKey是Email字段
        '''
        user_object = User(email='abc@163.com')
        self.assertEqual(user_object.pk, 'abc@163.com')


    def test_no_problem_with_auth_login(self):
        ''' 可以正常使用Django提供的login()函数
        '''
        user_object = User.objects.create(email='abc@163.com')
        user_object.backend = ''
        request = self.client.request().wsgi_request
        login(request, user_object)     ## 这里不会出现异常


class TokenModelTest(TestCase):
    ''' 登录验证模型
    '''
    def test_email_is_primary_key(self):
        ''' 登录验证模型的PrimaryKey是Email字段
        '''
        token_object = Token(email='abc@163.com')
        self.assertEqual(token_object.pk, 'abc@163.com')

