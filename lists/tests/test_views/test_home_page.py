#!python
# coding: utf-8
#------------------------------
# lists.tests.test_views.test_home_page
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
from django.test import TestCase

from lists.forms import ItemForm


class HomePageTest(TestCase):
    ''' 首页测试
    '''
    def test_001(self):
        ''' 首页显示页面
        '''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/index.html')

    def test_002(self):
        ''' 首页显示上下文
        '''
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

