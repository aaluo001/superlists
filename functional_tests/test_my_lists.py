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
User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        user_object = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user_object.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        
        ## 为了设定cookie，我们要先访问网站
        ## 而404页面加载最快
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))


    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'abc@163.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)
        
        ## 测试已经是登录用户了
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)


