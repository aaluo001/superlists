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
    ''' ���͵�¼��֤�ʼ����ܲ���
    '''
    def post_send_login_email(self):
        return self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'})


    def test_001(self):
        ''' �����ʼ���ҳ����ת����ҳ
        '''
        response = self.post_send_login_email()
        self.assertRedirects(response, '/')


    def test_002(self):
        ''' �����ʼ���Token���е�Email��ַ���ύEmail��ַһ��
        '''
        self.post_send_login_email()
        token_object = Token.objects.first()
        self.assertEqual(token_object.email, 'abc@163.com')


    def test_003(self):
        ''' ��ͬһ�����ַ���������ʼ�
            �������ַ��Token����ֻ��һ������
            Token�����������ɵ�UID��һ��
        '''
        self.post_send_login_email()
        uid_1 = Token.objects.first().uid
        self.post_send_login_email()
        uid_2 = Token.objects.first().uid
        
        self.assertEqual(Token.objects.count(), 1)
        self.assertNotEqual(uid_1, uid_2)


    @patch('accounts.views.send_mail')
    def test_004(self, mock_send_mail):
        ''' �����ʼ�ʱʹ����send_mail()����
        '''
        self.post_send_login_email()
        
        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(SUBJECT, subject)
        self.assertIn('���Ǹ���������һ�����ӣ�������ʹ���������ӽ��е�¼', body)
        self.assertIn('���Ǹ���������һ�����ӣ�������ʹ���������ӽ��е�¼', kwargs['html_message'])
        self.assertEqual(from_email, 'superlists@163.com')
        self.assertEqual(to_list, ['abc@163.com', ])


    @patch('accounts.views.send_mail')
    def test_005(self, mock_send_mail):
        ''' �����ʼ������������¼��֤������
        '''
        self.post_send_login_email()
        
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        token_object = Token.objects.first()
        excepted_url = 'http://testserver/accounts/login?token={}'.format(token_object.uid)
        self.assertIn(excepted_url, body)


    @patch('accounts.views.messages')
    def test_006(self, mock_messages):
        ''' �����ʼ��ɹ���ִ����messages.success()����
        '''
        response = self.post_send_login_email()
        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, SEND_EMAIL_SUCCESSED)
        )


    @patch('accounts.views.send_mail')
    @patch('accounts.views.messages')
    def test_007(self, mock_messages, mock_send_mail):
        ''' �����ʼ����ܺ�ִ����messages.error()����
        '''
        mock_send_mail.side_effect = smtplib.SMTPRecipientsRefused('Send mail error!')
        response = self.post_send_login_email()
        self.assertEqual(
            mock_messages.error.call_args,
            call(response.wsgi_request, SEND_EMAIL_FAILED)
        )


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    ''' ��¼���ܲ���
    '''
    def get_login(self):
        return self.client.get('/accounts/login?token=abc123')


    def test_001(self, mock_auth):
        ''' ��¼��ҳ����ת����ҳ
        '''
        response = self.get_login()
        self.assertRedirects(response, '/')


    def test_002(self, mock_auth):
        ''' ��¼��֤ʱ��ʹ����auth.authenticate()����
        '''
        self.get_login()
        self.assertEqual(mock_auth.authenticate.call_args, call(uid='abc123'))


    def test_003(self, mock_auth):
        ''' ��¼��֤�ɹ���ִ����auth.login()����
        '''
        response = self.get_login()
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )


    @patch('accounts.views.messages')
    def test_004(self, mock_messages, mock_auth):
        ''' ��¼��֤ʧ��ʱ��û��ִ��auth.login()��������Ҫִ����messages.error()����
        '''
        mock_auth.authenticate.return_value = None
        response = self.get_login()
        self.assertEqual(mock_auth.login.called, False)
        self.assertEqual(
            mock_messages.error.call_args,
            call(response.wsgi_request, LOGIN_FAILED)
        )

