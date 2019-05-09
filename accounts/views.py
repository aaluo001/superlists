#!python
# coding: gbk
#------------------------------
# accounts.views.py
#------------------------------
# author: TangJianwei
# update: 2019-03-25
#------------------------------
import uuid
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages, auth

from accounts.models import Token


SUBJECT = '���Ǹ���������һ����¼��֤�õ�����'

TEXT_MESSAGE = '''
    ���ã�\n
    ���� Superlists ��վ���������������ַ���е�¼��֤��\n
    Ϊ�����Ǹ���������һ�����ӣ�������ʹ���������ӽ��е�¼��\n
    {0}
'''

HTML_MESSAGE = '''
    <html>
    <body>
        ���ã�<br>
        ���� Superlists ��վ���������������ַ���е�¼��֤��<br>
        Ϊ�����Ǹ���������һ�����ӣ�������ʹ���������ӽ��е�¼��<br>
        <a href="{0}" target="_blank">{0}</a>
    </body>
    </html>
'''

FROM_EMAIL = 'superlists@163.com'

SEND_EMAIL_SUCCESSED = '''
    �ʼ����ͳɹ���
    ���������ʼ����ݣ����Ǹ���������һ�����ӣ�������ʹ���������ӽ��е�¼��
'''

LOGIN_FAILED = '''
    ��¼ʧ�ܣ�
    ��ȷ�����ĵ�¼�����Ƿ���ȷ���������������ʼ���ַ���е�¼��
'''


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
    send_mail(SUBJECT, text_message, FROM_EMAIL, [email, ], html_message=html_message)

    messages.success(request, SEND_EMAIL_SUCCESSED)
    return redirect('/')


def login(request):
    user_object = auth.authenticate(uid=request.GET.get('token'))
    if (user_object):
        auth.login(request, user_object)
    else:
        messages.error(request, LOGIN_FAILED)
    return redirect('/')
