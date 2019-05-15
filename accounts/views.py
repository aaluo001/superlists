#!python
# coding: gbk
#------------------------------
# accounts.views
#------------------------------
# Author: TangJianwei
# Create: 2019-03-25
#------------------------------
import uuid
import smtplib

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages, auth

from accounts.models import Token


SUBJECT = '我们给您发送了一条登录验证的链接'

TEXT_MESSAGE = '''
    您好！\n
    您在 Superlists 网站输入了您的邮箱地址进行登录验证，\n
    为此我们给您发送了一条链接，您可以使用这条链接进行登录：\n
    {0}
'''

HTML_MESSAGE = '''
    <html>
    <body>
        您好！<br>
        您在 Superlists 网站输入了您的邮箱地址进行登录验证，<br>
        为此我们给您发送了一条链接，您可以使用这条链接进行登录：<br>
        <a href="{0}" target="_blank">{0}</a>
    </body>
    </html>
'''

FROM_EMAIL = 'superlists@163.com'

SEND_EMAIL_SUCCESSED = '邮件发送成功！请检查您的邮件内容，我们给您发送了一条链接，您可以使用这条链接进行登录。'
SEND_EMAIL_FAILED    = '邮件发送失败！请检查您的邮箱地址是否正确。'
LOGIN_FAILED         = '登录失败！请确认您的登录链接是否正确，或是重新输入邮箱地址进行登录。'


def send_login_email(request):
    email = request.POST['email']
    token_object = None
    try:
        token_object = Token.objects.get(email=email)
        token_object.uid = uuid.uuid4()
        token_object.save()
    
    except Token.DoesNotExist:
        token_object = Token.objects.create(email=email, uid=uuid.uuid4())

    url = request.build_absolute_uri(
        reverse('login') + '?token={}'.format(token_object.uid)
    )
    text_message = TEXT_MESSAGE.format(url)
    html_message = HTML_MESSAGE.format(url)
    
    try:
        send_mail(SUBJECT, text_message, FROM_EMAIL, [email, ], html_message=html_message)
    except smtplib.SMTPRecipientsRefused:
        messages.error(request, SEND_EMAIL_FAILED)
    else:
        messages.success(request, SEND_EMAIL_SUCCESSED)
    
    return redirect('/')


def login(request):
    user_object = auth.authenticate(uid=request.GET.get('token'))
    if (user_object):
        auth.login(request, user_object)
    else:
        messages.error(request, LOGIN_FAILED)
    return redirect('/')
