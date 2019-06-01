#!python
# coding: gbk
#------------------------------
# functional_tests.test_send_login_email_validation
#------------------------------
# Author: TangJianwei
# Create: 2019-05-18
#------------------------------
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class SendLoginEmailValidationTest(FunctionalTest):
    ''' ���͵�¼�ʼ���֤����
    '''
    def test_001(self):
        ''' δ���������ַ�ͷ����ʼ�
        '''
        # ������ҳ
        # δ���������ַ�ͷ����ʼ�
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(Keys.ENTER)

        # ������ػ�������ҳ�治�ᱻ����
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:invalid')
        )


    def test_002(self):
        ''' ���ʹ��������ַ����õ������ʼ�ʧ�ܵ���ʾ
            ���������Server Error (500)
        '''
        # ֻ���ڹ�����վ�в���
        if (not self.staging_tests): return
        
        # ������ҳ
        # �ڵ������ĵ�¼�����������������ַ
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys('error_email_tests@163.com')
        input_email.send_keys(Keys.ENTER)
        
        # ��⵽���ʼ�����ʧ�ܡ�����Ϣ
        self.wait_for(lambda: self.assertIn(
            '�ʼ�����ʧ��',
            self.browser.find_element_by_id('id_messages').text
        ))

        # û�м�⵽��ServerError(500)��
        self.assertNotIn('Server Error (500)', self.browser.page_source)

