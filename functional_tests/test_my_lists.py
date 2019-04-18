#!python
# coding: gbk
#------------------------------
# test_my_lists.py
#------------------------------
# author: TangJianwei
# update: 2019-04-04
#------------------------------
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import (
    get_user_model,
    BACKEND_SESSION_KEY, SESSION_KEY,
)

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if (self.staging_tests):
            session_key = create_session_on_server(email)
        else:
            session_key = create_pre_authenticated_session(email)
        
        ## Ϊ���趨cookie������Ҫ�ȷ�����վ
        ## ��404ҳ��������
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))


    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'abc@163.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)
        
        ## �����Ѿ��ǵ�¼�û���
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

