#!python
# coding: gbk
#------------------------------
# test_login.py
#------------------------------
# author: TangJianwei
# update: 2019-03-23
#------------------------------
import re
from django.core import mail

from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


TEST_EMAIL = 'abc@163.com'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_login(self):
        # ����Ӧ����ҳ
        # ���ֵ������еĵ�¼����
        # ���ǣ���������ʼ���ַ
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(TEST_EMAIL)
        input_email.send_keys(Keys.ENTER)
        
        # ����һ����Ϣ����ʾ�����ʼ��Ѿ�����ȥ��
        self.wait_for(lambda: self.assertIn(
            '�ʼ����ͳɹ�',
            self.browser.find_element_by_tag_name('body').text
        ))
        
        # �鿴�����ʼ�
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertIn('���Ǹ���������һ����¼��֤�õ�����', email.subject)
        self.assertIn('Ϊ�����Ǹ���������һ�����ӣ�������ʹ���������ӽ��е�¼', email.body)

        # �ʼ����и�URL����
        url_search = re.search('http://.+/accounts/login\?token=.+$', email.body)
        if (not url_search):
            self.fail('Could not find url in email body: \n{}'.format(email.body))
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        
        # �������
        self.browser.get(url)
        
        # ��¼�ɹ�
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # �˳���¼
        self.browser.find_element_by_link_text('�˳�').click()

        # �˳��ɹ�
        self.wait_to_be_logged_out(email=TEST_EMAIL)

