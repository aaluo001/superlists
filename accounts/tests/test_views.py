#!python
# coding: gbk
#------------------------------
# accounts.tests.test_views
#------------------------------
# Author: TangJianwei
# Create: 2019-03-25
#------------------------------
from unittest.mock import patch, call
from django.test import TestCase

from accounts.views import (
    SUBJECT, SEND_EMAIL_SUCCESSED, LOGIN_FAILED
)
from accounts.models import Token
import accounts.views



class SendLoginEmailViewTest(TestCase):
    ''' 发送登录验证邮件机能
    '''
    def test_redirects_to_home_page(self):
        ''' 发送邮件后，页面跳转到首页
        '''
        response = self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'},
        )
        self.assertRedirects(response, '/')


    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        ''' 输入登录邮件地址提交后，执行了send_mail()函数
        '''
        self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'},
        )

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(SUBJECT, subject)
        self.assertIn('我们给您发送了一条链接，您可以使用这条链接进行登录', body)
        self.assertIn('我们给您发送了一条链接，您可以使用这条链接进行登录', kwargs['html_message'])
        self.assertEqual(from_email, 'superlists@163.com')
        self.assertEqual(to_list, ['abc@163.com', ])


    @patch('accounts.views.messages')
    def test_adds_success_message(self, mock_messages):
        ''' 输入登录邮件地址提交后，执行了messages.success()函数
        '''
        response = self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'},
        )
        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, SEND_EMAIL_SUCCESSED)
        )


    def test_creates_token_associated_with_email(self):
        ''' 输入登录邮件地址提交后，Token表会有该Email的用户
            Token表中该Email用户不存在时，就新建
        '''
        response = self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'},
        )
        token_object = Token.objects.first()
        self.assertEqual(token_object.email, 'abc@163.com')


    def test_updates_token_associated_when_email_is_exist(self):
        ''' 输入登录邮件地址提交后，Token表会有该Email的用户
            Token表中该Email用户已经存在时，就直接更新
            且用户的UID与新建时，不一样
        '''
        response = self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'},
        )
        uid_1 = Token.objects.get(email='abc@163.com').uid

        response = self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'},
        )
        uid_2 = Token.objects.get(email='abc@163.com').uid
        
        self.assertNotEqual(uid_1, uid_2)


    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        ''' 输入登录邮件地址提交后，发送邮件内容里包含登录验证的链接
        '''
        reponse = self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'},
        )
        
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        token_object = Token.objects.first()
        excepted_url = 'http://testserver/accounts/login?token={}'.format(token_object.uid)
        self.assertIn(excepted_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    ''' 登录机能
    '''
    def test_redirects_to_home_page(self, mock_auth):
        ''' 登录后，页面跳转到首页
        '''
        response = self.client.get('/accounts/login?token=abc123')
        self.assertRedirects(response, '/')


    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        ''' 登录时，执行了auth.authenticate()函数
        '''
        response = self.client.get('/accounts/login?token=abc123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abc123')
        )


    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        ''' 登录时，如果验证成功，就执行auth.login()函数
        '''
        response = self.client.get('/accounts/login?token=abc123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )


    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        ''' 登录时，如果验证失败，就不执行auth.login()函数
        '''
        mock_auth.authenticate.return_value = None
        response = self.client.get('/accounts/login?token=abc123')
        self.assertEqual(mock_auth.login.called, False)


    @patch('accounts.views.messages')
    def test_adds_error_messages_if_user_is_not_authenticated(self, mock_messages, mock_auth):
        ''' 登录时，如果验证失败，就会执行messages.error()函数
            注意：函数的参数mock_messages一定要写在mock_auth的前面，与patch()的执行顺序相反
        '''
        mock_auth.authenticate.return_value = None
        response = self.client.get('/accounts/login?token=abc123')
        self.assertEqual(
            mock_messages.error.call_args,
            call(response.wsgi_request, LOGIN_FAILED)
        )

