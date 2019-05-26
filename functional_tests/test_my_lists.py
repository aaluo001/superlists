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
        
        ## 为了设定cookie，我们要先访问网站
        ## 而404页面加载最快
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))


    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        ## 测试已经是登录用户了
        self.create_pre_authenticated_session('abc@163.com')
        
        # 访问首页，新建一个清单
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url
        
        # 出现"待办事项清单"的链接
        self.browser.find_element_by_link_text("待办事项清单").click()
        
        # 待办事项清单页面有刚刚新建的清单
        # 而且清单根据第一个待办事项命名
        self.wait_for(lambda:
            self.browser.find_element_by_link_text('Reticulate splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, first_list_url)
        )
        
        # 再建一个待办事项清单
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url
        
        # 在"待办事项清单"里面可以看见这个新建的清单
        self.browser.find_element_by_link_text("待办事项清单").click()
        self.wait_for(lambda:
            self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(lambda:
            self.assertEqual(self.browser.current_url, second_list_url)
        )

        # 退出后，"待办事项清单"链接不见了
        self.browser.find_element_by_link_text("退出").click()
        self.wait_for(lambda:
            self.assertEqual(
                self.browser.find_elements_by_link_text("待办事项清单"),
                []
            )
        )

