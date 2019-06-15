#------------------------------
# lists.tests.test_views.test_my_lists
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import List, Item


class MyListsTest(TestCase):
    ''' 我的清单测试
    '''
    def test_001(self):
        ''' 我的清单显示页面
        '''
        user_object = User.objects.create(email='abc@163.com')
        self.client.force_login(user_object)
        response = self.client.get('/lists/')
        self.assertTemplateUsed(response, 'lists/my_lists.html')


    def test_002(self):
        ''' 我的清单上下文
        '''
        user_object = User.objects.create(email='abc@163.com')
        list_object_1 = List.objects.create(owner=user_object)
        Item.objects.create(list=list_object_1, text='New item 1')
        list_object_2 = List.objects.create(owner=user_object)
        Item.objects.create(list=list_object_2, text='New item 2')
        
        other_list_object = List.objects.create()
        Item.objects.create(list=other_list_object, text='Other item')

        self.client.force_login(user_object)
        response = self.client.get('/lists/')
        
        list_set = response.context['list_set']
        self.assertEqual(len(list_set), 2)
        self.assertIn(list_object_1, list_set)
        self.assertIn(list_object_2, list_set)
        self.assertNotIn(other_list_object, list_set)

    
    def test_003(self):
        ''' 没有清单时不会报错
        '''
        user_object = User.objects.create(email='abc@163.com')
        self.client.force_login(user_object)
        response = self.client.get('/lists/')
        self.assertEqual(len(user_object.list_set.all()), 0)
        self.assertEqual(len(response.context['list_set']), 0)
        
        
    def test_004(self):
        ''' 匿名用户直接跳转到首页
        '''
        response = self.client.get('/lists/')
        self.assertRedirects(response, '/')

