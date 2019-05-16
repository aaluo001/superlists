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
    ''' ���͵�¼��֤�ʼ�����
    '''
    def post_send_login_email(self):
        return self.client.post('/accounts/send_login_email', 
            data={'email': 'abc@163.com'})


    def test_redirects_to_home_page(self):
        ''' �����ʼ���ҳ����ת����ҳ
        '''
        response = self.post_send_login_email()
        self.assertRedirects(response, '/')


    def test_creates_token_associated_with_email(self):
        ''' �����¼�ʼ���ַ�ύ��Token����и�Email���û�
            Token���и�Email�û�������ʱ�����½�
        '''
        self.post_send_login_email()
        token_object = Token.objects.first()
        self.assertEqual(token_object.email, 'abc@163.com')

    def test_updates_token_associated_when_email_is_exist(self):
        ''' �����¼�ʼ���ַ�ύ��Token����и�Email���û�
            Token���и�Email�û��Ѿ�����ʱ����ֱ�Ӹ���
            ���û���UID���½�ʱ����һ��
        '''
        self.post_send_login_email()
        uid_1 = Token.objects.get(email='abc@163.com').uid
        self.post_send_login_email()
        uid_2 = Token.objects.get(email='abc@163.com').uid
        self.assertNotEqual(uid_1, uid_2)


    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        ''' �����¼�ʼ���ַ�ύ��ִ����send_mail()����
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
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        ''' �����¼�ʼ���ַ�ύ�󣬷����ʼ������������¼��֤������
        '''
        self.post_send_login_email()
        
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        token_object = Token.objects.first()
        excepted_url = 'http://testserver/accounts/login?token={}'.format(token_object.uid)
        self.assertIn(excepted_url, body)


    @patch('accounts.views.messages')
    def test_adds_success_message(self, mock_messages):
        ''' �����¼�ʼ���ַ�ύ��ִ����messages.success()����
        '''
        response = self.post_send_login_email()
        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, SEND_EMAIL_SUCCESSED)
        )

    @patch('accounts.views.send_mail')
    @patch('accounts.views.messages')
    def test_adds_error_message_when_SMTPRecipientsRefused(self, mock_messages, mock_send_mail):
        ''' �����¼�ʼ���ַ�ύ��ִ����messages.success()����
        '''
        mock_send_mail.side_effect = smtplib.SMTPRecipientsRefused('Send mail error!')
        response = self.post_send_login_email()
        self.assertEqual(
            mock_messages.error.call_args,
            call(response.wsgi_request, SEND_EMAIL_FAILED)
        )


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    ''' ��¼����
    '''
    def get_login(self):
        return self.client.get('/accounts/login?token=abc123')


    def test_redirects_to_home_page(self, mock_auth):
        ''' ��¼��ҳ����ת����ҳ
        '''
        response = self.get_login()
        self.assertRedirects(response, '/')


    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        ''' ��¼ʱ��ִ����auth.authenticate()����
        '''
        self.get_login()
        self.assertEqual(mock_auth.authenticate.call_args, call(uid='abc123'))

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        ''' ��¼ʱ�������֤�ɹ�����ִ��auth.login()����
        '''
        response = self.get_login()
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    @patch('accounts.views.messages')
    def test_adds_error_messages_if_user_is_not_authenticated(self, mock_messages, mock_auth):
        ''' ��¼ʱ�������֤ʧ�ܣ��Ͳ�ִ��auth.login()��������Ҫִ��messages.error()����
            ע�⣺�����Ĳ���mock_messagesһ��Ҫд��mock_auth��ǰ�棬��patch()��ִ��˳���෴
        '''
        mock_auth.authenticate.return_value = None
        response = self.get_login()
        self.assertEqual(mock_auth.login.called, False)
        self.assertEqual(
            mock_messages.error.call_args,
            call(response.wsgi_request, LOGIN_FAILED)
        )

