#!python
# coding: gbk
#------------------------------
# create_session.py
#------------------------------
# author: TangJianwei
# update: 2019-04-14
#------------------------------
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import (
    get_user_model, BACKEND_SESSION_KEY, SESSION_KEY,
)
from django.core.management.base import BaseCommand


User = get_user_model()


def create_pre_authenticated_session(email):
    try:
        user_object = User.objects.get(email=email)
    except User.DoesNotExist:
        user_object = User.objects.create(email=email)

    session = SessionStore()
    session[SESSION_KEY] = user_object.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key


class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('email')

    def handle(self, *args, **kwargs):
        session_key = create_pre_authenticated_session(kwargs['email'])
        self.stdout.write(session_key)

