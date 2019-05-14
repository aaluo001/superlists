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
    SUBJECT, SEND_EMAIL_SUCCESSED
)
from accounts.models import Token
import accounts.views



class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'},
        )
        self.assertRedirects(response, '/')


    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'},
        )

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(SUBJECT, subject)
        self.assertIn('为此我们给您发送了一条链接，您可以使用这条链接进行登录', body)
        self.assertIn('为此我们给您发送了一条链接，您可以使用这条链接进行登录', kwargs['html_message'])
        self.assertEqual(from_email, 'superlists@163.com')
        self.assertEqual(to_list, ['abc@163.com', ])


    @patch('accounts.views.messages')
    def test_adds_success_message(self, mock_messages):
        response = self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'},
        )
        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, SEND_EMAIL_SUCCESSED)
        )


    def test_creates_token_associated_with_email(self):
        response = self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'},
        )
        token_object = Token.objects.first()
        self.assertEqual(token_object.email, 'abc@163.com')


    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        reponse = self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'},
        )
        
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        token_object = Token.objects.first()
        excepted_url = 'http://testserver/accounts/login?token={}'.format(token_object.uid)
        self.assertIn(excepted_url, body)



@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    
    def test_redirects_to_home_pate(self, mock_auth):
        response = self.client.get('/accounts/login?token=abc123')
        self.assertRedirects(response, '/')


    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        response = self.client.get('/accounts/login?token=abc123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abc123')
        )


    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get('/accounts/login?token=abc123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )


    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abc123')
        self.assertEqual(mock_auth.login.called, False)

