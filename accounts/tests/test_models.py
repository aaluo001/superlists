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
    ''' �����û�ģ��
    '''
    def test_user_is_valid_with_email_only(self):
        ''' ȷ���û���������ʹ�ã����ֻ����Email�Ļ�
        '''
        user_object = User(email='abc@163.com')
        user_object.full_clean()   # ��������쳣


    def test_email_is_primary_key(self):
        ''' ȷ���û�ģ�͵�PrimaryKey��Email
        '''
        user_object = User(email='abc@163.com')
        self.assertEqual(user_object.pk, 'abc@163.com')


    def test_no_problem_with_auth_login(self):
        ''' ȷ��ʹ��Django�ṩ��login���ܿ�������ʹ��
        '''
        user_object = User.objects.create(email='abc@163.com')
        user_object.backend = ''
        request = self.client.request().wsgi_request
        login(request, user_object) # ��������쳣


class TokenModelTest(TestCase):
    ''' ���Ե�¼��֤ģ��
    '''
    def test_email_is_primary_key(self):
        ''' ȷ����¼��֤ģ�͵�PrimaryKey��Email
        '''
        token_object = Token(email='abc@163.com')
        self.assertEqual(token_object.pk, 'abc@163.com')

