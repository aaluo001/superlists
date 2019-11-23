#------------------------------
# bills.tests.test_views.test_select_billym
#------------------------------
# Author: TangJianwei
# Create: 2019-11-21
#------------------------------
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

from bills.models import Billym, Bill


class SelectBillymTest(TestCase):

    def test_001(self):
        ''' 只有登录用户才是使用该机能，未登录用户会跳转到首页
        '''
        owner = User.objects.create(email='abc@163.com')
        billym = Billym.objects.create(owner=owner, year=2019, month=1)

        # 未登录用户会跳转到首页
        response = self.client.get(reverse('bills:select_billym', args=[billym.id,]))
        self.assertRedirects(response, '/')

        # 登录用户可以使用该机能，并迁移到selected_billym页面
        self.client.force_login(owner)
        response = self.client.get(reverse('bills:select_billym', args=[billym.id,]))
        self.assertTemplateUsed(response, 'bills/selected_billym.html')

    def test_002(self):
        ''' 上下文
        '''
        owner = User.objects.create(email='abc@163.com')
        billym_1 = Billym.objects.create(owner=owner, year=2019, month=1)
        billym_2 = Billym.objects.create(owner=owner, year=2019, month=2)

        self.client.force_login(owner)
        response = self.client.get(reverse('bills:select_billym', args=[billym_1.id,]))
        self.assertEquals(response.context['selected_billym'], billym_1)
        response = self.client.get(reverse('bills:select_billym', args=[billym_2.id,]))
        self.assertEquals(response.context['selected_billym'], billym_2)

        self.assertEquals('Finished the test！', '')
