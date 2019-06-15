#------------------------------
# lists.tests.test_views.test_remove_list
#------------------------------
# Author: TangJianwei
# Create: 2019-05-26
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import List, Item


class RemoveListTest(TestCase):
    ''' 删除清单测试
    '''
    def test_001(self):
        ''' 删除清单后跳转到我的清单
        '''
        user_object = User.objects.create(email='abc@163.com')
        self.client.force_login(user_object)
        list_object = List.objects.create(owner=user_object)
        Item.objects.create(list=list_object, text='New item')
        response = self.client.get('/lists/{}/remove'.format(list_object.pk))
        self.assertRedirects(response, '/lists/')


    def test_002(self):
        ''' 删除清单的同时，也删除了该清单的待办事项
        '''
        user_object = User.objects.create(email='abc@163.com')
        self.client.force_login(user_object)
        list_object = List.objects.create(owner=user_object)
        item_object_1 = Item.objects.create(list=list_object, text='New item 1')
        item_object_2 = Item.objects.create(list=list_object, text='New item 2')
        
        self.assertEqual(Item.objects.count(), 2)
        self.assertIn(item_object_1, list_object.item_set.all())
        self.assertIn(item_object_2, list_object.item_set.all())
        
        response = self.client.get('/lists/{}/remove'.format(list_object.pk))
        
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)
        self.assertNotIn(list_object, user_object.list_set.all())
    
    
    def test_003(self):
        ''' 没有找到清单时不会报错，页面也会跳转到我的清单
        '''
        user_object = User.objects.create(email='abc@163.com')
        self.client.force_login(user_object)
        response = self.client.get('/lists/999/remove')
        self.assertRedirects(response, '/lists/')
        
        
    def test_004(self):
        ''' 匿名用户直接跳转到首页
        '''
        user_object = User.objects.create(email='abc@163.com')
        # 未登录用户
        # self.client.force_login(user_object)
        list_object = List.objects.create(owner=user_object)
        item_object_1 = Item.objects.create(list=list_object, text='New item 1')
        item_object_2 = Item.objects.create(list=list_object, text='New item 2')
        response = self.client.get('/lists/{}/remove'.format(list_object.pk))
        
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(List.objects.count(), 1)
        self.assertIn(list_object, user_object.list_set.all())
        self.assertRedirects(response, '/')


