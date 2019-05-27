#!python
# coding: gbk
#------------------------------
# functional_tests.test_my_lists
#------------------------------
# Author: TangJianwei
# Create: 2019-04-04
#------------------------------
import time
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.auth import get_user_model
User = get_user_model()

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListsTest(FunctionalTest):
    ''' �ҵ��嵥����
    '''
    def create_pre_authenticated_session(self, email):
        if (self.staging_tests):
            session_key = create_session_on_server(email)
        else:
            session_key = create_pre_authenticated_session(email)
        
        # Ϊ���趨Cookie������Ҫ�ȷ�����վ
        # ��404ҳ��������
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))


    def test_001(self):
        ''' ��¼�û������½��嵥��Ȼ�����ҵ��嵥ҳ����ʾ
        '''
        # ������¼�û�
        self.create_pre_authenticated_session('abc@163.com')
        
        # �½��嵥
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        list_url_1 = self.browser.current_url

        # ���"�ҵ��嵥"����
        self.browser.find_element_by_link_text('��������').click()
        self.browser.find_element_by_link_text('�ҵ��嵥').click()

        # ��Ļ��ʾ"�ҵ��嵥"
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('div.text-center > h1').text,
            '�ҵ��嵥'
        ))

        # �ҵ��嵥ҳ������½����嵥
        # ���嵥�����ǵ�һ���������������
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('table#id_my_lists_table')
        )
        self.wait_for(lambda:
            self.browser.find_element_by_link_text('Reticulate splines')
        )

        # �����嵥ҳ�棬��ҳ������Ӻ��½��嵥������һ��
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, list_url_1)
        )

        
        # --- ���½�һ�����������嵥 ---

        # ���"�½��嵥"����
        self.browser.find_element_by_link_text('��������').click()
        self.browser.find_element_by_link_text('�½��嵥').click()
        
        # �½��嵥
        self.add_list_item('Click cows')
        list_url_2 = self.browser.current_url

        # ���"�ҵ��嵥"����
        self.browser.find_element_by_link_text('��������').click()
        self.browser.find_element_by_link_text('�ҵ��嵥').click()

        # �ҵ��嵥ҳ������½����嵥
        # ���嵥�����ǵ�һ���������������
        self.wait_for(lambda:
            self.browser.find_element_by_link_text('Click cows')
        )
        
        # �����嵥ҳ�棬��ҳ������Ӻ��½��嵥������һ��
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, list_url_2)
        )

        # �˳���"�ҵ��嵥"���Ӳ�����
        self.browser.find_element_by_link_text("�˳�").click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text("�ҵ��嵥"),
            []
        ))

        
    def test_002(self):
        ''' ��¼�û�û�д����嵥ʱ���ҵ��嵥ҳ��û���嵥��ʾ
        '''
        # ������¼�û�
        self.create_pre_authenticated_session('abc@163.com')
        self.browser.get(self.live_server_url)

        # ���"�ҵ��嵥"����
        self.browser.find_element_by_link_text('��������').click()
        self.browser.find_element_by_link_text('�ҵ��嵥').click()

        # ��Ļ��ʾ"�ҵ��嵥"
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('div.text-center > h1').text,
            '�ҵ��嵥'
        ))
        
        # û���嵥��ʾ
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_css_selector('table#id_my_lists_table'),
            []
        ))
        
        # ��ʾû���嵥����Ϣ
        self.wait_for(lambda: self.assertIn(
            '����û���Լ����嵥',
            self.browser.find_element_by_tag_name('body').text
        ))

    
    def test_003(self):
        ''' �����û��޷���ʾ�ҵ��嵥
        '''
        # �����û��½��嵥
        self.browser.get(self.live_server_url)
        self.add_list_item('Work at office')
        self.add_list_item('Have a dinner')
        
        # û���ҵ�"��������"�˵�
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('��������'),
            []
        ))

        # ʹ��URL��ַǿ�н���"�ҵ��嵥"
        self.browser.get(self.live_server_url + '/lists/')

        # ҳ����ת����ҳ
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('div.text-center > h1').text,
            '�½��嵥'
        ))
        self.assertEqual(self.browser.current_url, self.live_server_url + '/')

