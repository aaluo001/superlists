#!python
# coding: gbk
#------------------------------
# accounts.views.py
#------------------------------
# author: TangJianwei
# update: 2019-03-25
#------------------------------
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages, auth

from accounts.models import Token


SUBJECT = '[Superlists]��¼��֤'

MESSAGE_BODY = '''
    ��ʹ����������ӽ��е�¼��֤: \n\n{}
'''

FROM_EMAIL = 'superlists@163.com'

SEND_EMAIL_SUCCESSED = '''
    �ʼ����ͳɹ���
    ���������ʼ����ݣ����Ǹ���������һ�����ӣ�������ʹ���������ӵ�¼������վ��
'''


def send_login_email(request):
    email = request.POST['email']
    token_object = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token={}'.format(token_object.uid)
    )
    send_mail(SUBJECT, MESSAGE_BODY.format(url), FROM_EMAIL, [email])
    messages.success(request, SEND_EMAIL_SUCCESSED)
    return redirect('/')


def login(request):
    user_object = auth.authenticate(uid=request.GET.get('token'))
    if (user_object): auth.login(request, user_object)
    return redirect('/')
