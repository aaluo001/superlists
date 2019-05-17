#!python
# coding: gbk
#------------------------------
# accounts.tests.test_views
#------------------------------
# Author: TangJianwei
# Create: 2019-03-25
#------------------------------
import smtplib
from unittest.mock import patch, call
from django.test import TestCase

from accounts.views import (
    SUBJECT, SEND_EMAIL_SUCCESSED, SEND_EMAIL_FAILED, LOGIN_FAILED
)
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
    ''' 发送登录验证邮件机能测试
    '''
    def post_send_login_email(self):
        return self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'})


    def test_001(self):
        ''' 发送邮件后，页面跳转到首页
        '''
        response = self.post_send_login_email()
        self.assertRedirects(response, '/')


    def test_002(self):
        ''' 发送邮件后，Token表中的Email地址与提交Email地址一致
        '''
        self.post_send_login_email()
        token_object = Token.objects.first()
        self.assertEqual(token_object.email, 'abc@163.com')


    def test_003(self):
        ''' 对同一邮箱地址发送两次邮件
            该邮箱地址在Token表中只有一条数据
            Token表中两次生成的UID不一致
        '''
        self.post_send_login_email()
        uid_1 = Token.objects.first().uid
        self.post_send_login_email()
        uid_2 = Token.objects.first().uid
        
        self.assertEqual(Token.objects.count(), 1)
        self.assertNotEqual(uid_1, uid_2)


    @patch('accounts.views.send_mail')
    def test_004(self, mock_send_mail):
        ''' 发送邮件时使用了send_mail()函数
        '''
        self.post_send_login_email()
        
        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(SUBJECT, subject)
        self.assertIn('我们给您发送了一条链接，您可以使用这条链接进行登录', body)
        self.assertIn('我们给您发送了一条链接，您可以使用这条链接进行登录', kwargs['html_message'])
        self.assertEqual(from_email, 'superlists@163.com')
        self.assertEqual(to_list, ['abc@163.com', ])


    @patch('accounts.views.send_mail')
    def test_005(self, mock_send_mail):
        ''' 发送邮件内容里包含登录验证的链接
        '''
        self.post_send_login_email()
        
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        token_object = Token.objects.first()
        excepted_url = 'http://testserver/accounts/login?token={}'.format(token_object.uid)
        self.assertIn(excepted_url, body)


    @patch('accounts.views.messages')
    def test_006(self, mock_messages):
        ''' 发送邮件成功后，执行了messages.success()函数
        '''
        response = self.post_send_login_email()
        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, SEND_EMAIL_SUCCESSED)
        )


    @patch('accounts.views.send_mail')
    @patch('accounts.views.messages')
    def test_007(self, mock_messages, mock_send_mail):
        ''' 发送邮件被拒后，执行了messages.error()函数
        '''
        mock_send_mail.side_effect = smtplib.SMTPRecipientsRefused('Send mail error!')
        response = self.post_send_login_email()
        self.assertEqual(
            mock_messages.error.call_args,
            call(response.wsgi_request, SEND_EMAIL_FAILED)
        )


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    ''' 登录机能测试
    '''
    def get_login(self):
        return self.client.get('/accounts/login?token=abc123')


    def test_001(self, mock_auth):
        ''' 登录后，页面跳转到首页
        '''
        response = self.get_login()
        self.assertRedirects(response, '/')


    def test_002(self, mock_auth):
        ''' 登录验证时，使用了auth.authenticate()函数
        '''
        self.get_login()
        self.assertEqual(mock_auth.authenticate.call_args, call(uid='abc123'))


    def test_003(self, mock_auth):
        ''' 登录验证成功后，执行了auth.login()函数
        '''
        response = self.get_login()
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )


    @patch('accounts.views.messages')
    def test_004(self, mock_messages, mock_auth):
        ''' 登录验证失败时，没有执行auth.login()函数，而要执行了messages.error()函数
        '''
        mock_auth.authenticate.return_value = None
        response = self.get_login()
        self.assertEqual(mock_auth.login.called, False)
        self.assertEqual(
            mock_messages.error.call_args,
            call(response.wsgi_request, LOGIN_FAILED)
        )

