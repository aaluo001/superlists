#!python
# coding: gbk
#------------------------------
# functional_tests.test_my_lists
#------------------------------
# Author: TangJianwei
# Create: 2019-04-04
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
        ## �����Ѿ��ǵ�¼�û���
        self.create_pre_authenticated_session('abc@163.com')
        
        # ������ҳ���½�һ���嵥
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url
        
        # ����"���������嵥"������
        self.browser.find_element_by_link_text("���������嵥").click()
        
        # ���������嵥ҳ���иո��½����嵥
        # �����嵥���ݵ�һ��������������
        self.wait_for(lambda:
            self.browser.find_element_by_link_text('Reticulate splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, first_list_url)
        )
        
        # �ٽ�һ�����������嵥
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url
        
        # ��"���������嵥"������Կ�������½����嵥
        self.browser.find_element_by_link_text("���������嵥").click()
        self.wait_for(lambda:
            self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, second_list_url)
        )

        # �˳���"���������嵥"���Ӳ�����
        self.browser.find_element_by_link_text("�˳�").click()
        self.wait_for(lambda:
            self.assertEqual(
                self.browser.find_elements_by_link_text("���������嵥"),
                []
            )
        )

