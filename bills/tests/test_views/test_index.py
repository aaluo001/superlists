#------------------------------
# bills.tests.test_views.test_index
#------------------------------
# Author: TangJianwei
# Create: 2019-11-17
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from bills.models import Billym, Bill
from bills.forms import BillForm


class IndexTest(TestCase):

    def test_001(self):
        ''' 迁移到"index.html"页面
            只有登录用户才是使用该机能，未登录用户会跳转到首页
        '''
        # 未登录用户会跳转到首页
        response = self.client.get('/bills/index/')
        self.assertRedirects(response, '/')

        # 登录用户可以使用该机能
        self.client.force_login(User.objects.create(email='abc@163.com'))
        response = self.client.get('/bills/index/')
        self.assertTemplateUsed(response, 'bills/index.html')

    def test_002(self):
        ''' 上下文
        '''
        self.client.force_login(User.objects.create(email='abc@163.com'))
        response = self.client.get('/bills/index/')
        self.assertIsInstance(response.context['form'], BillForm)

