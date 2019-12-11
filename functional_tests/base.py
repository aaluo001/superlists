#------------------------------
# functional_tests.base
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.core import mail
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings

from .server_tools import STAGING_SERVER, reset_database, create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


# 等待服务器响应时间(10秒)
# 10秒足以捕获潜在的问题和不可预知的缓慢因素
MAX_WAIT = 10

def wait(func):
    def wrap(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return func(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if ((time.time() - start_time) > MAX_WAIT): raise e
                time.sleep(0.5)
    return wrap


class FunctionalTest(StaticLiveServerTestCase):
    ''' 功能测试（基类）
    '''
    def init_browser(self):
        self.browser = webdriver.Firefox()
    
    def quit_browser(self):
        try: self.browser.quit()
        except: pass

        
    def setUp(self):
        self.init_browser()

        self.staging_tests = False
        if (os.getenv('STAGING_TESTS') == 'yes'):
            self.staging_tests = True
        
        if (self.staging_tests):
            self.live_server_url = 'http://' + STAGING_SERVER
            reset_database()

    def tearDown(self):
        self.quit_browser()

        
    def create_pre_authenticated_session(self, email):
        if (self.staging_tests):
            session_key = create_session_on_server(email)
        else:
            session_key = create_pre_authenticated_session(email)
        
        # 为了设定Cookie，我们要先访问网站
        # 而404页面加载最快
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    @wait
    def wait_for(self, func):
        return func()


    def get_error_element(self):
        ''' 取得显示错误信息的元素
        '''
        return self.wait_for(lambda: 
            self.browser.find_element_by_css_selector('.has-error')
        )

