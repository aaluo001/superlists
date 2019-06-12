#!python
# coding: utf-8
#------------------------------
# lists.tests.test_views.test_remove_list_item
#------------------------------
# Author: TangJianwei
# Create: 2019-06-12
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import List, Item


class RemoveListItemTest(TestCase):
    ''' 删除清单项目测试
    '''
    def create_list(self, force_login=True):
        list_object = None
        if (force_login):
            user_object = User.objects.create(email='abc@163.com')
            self.client.force_login(user_object)
            list_object = List.objects.create(owner=user_object)
        else:
            list_object = List.objects.create()
        return list_object

        
    def test_001(self):
        ''' 没有完全删除清单项目时，跳转到清单项目显示页面
            且List以及其余的Item没有被删除
        '''
        list_object = self.create_list()
        item_object_1 = Item.objects.create(list=list_object, text='New item 1')
        item_object_2 = Item.objects.create(list=list_object, text='New item 2')
        
        response = self.client.get('/lists/{}/remove_item'.format(item_object_1.pk))
        
        self.assertRedirects(response, '/lists/{}/'.format(list_object.pk))
        self.assertIn(item_object_2, list_object.item_set.all())


    def test_002(self):
        ''' 完全删除清单项目时，跳转到我的清单页面
            且List也同时被删除
        '''
        list_object = self.create_list()
        item_object = Item.objects.create(list=list_object, text='New item 1')
        
        response = self.client.get('/lists/{}/remove_item'.format(item_object.pk))
        
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)
        self.assertRedirects(response, '/lists/')
    
    
    def test_003(self):
        ''' 没有找到清单时不会报错，页面也会跳转到我的清单
        '''
#        user_object = User.objects.create(email='abc@163.com')
#        self.client.force_login(user_object)
#        response = self.client.get('/lists/999/remove')
#        self.assertRedirects(response, '/lists/')
        
        
    def test_004(self):
        ''' 匿名用户直接跳转到首页
        '''
#        user_object = User.objects.create(email='abc@163.com')
#        # 未登录用户
#        # self.client.force_login(user_object)
#        list_object = List.objects.create(owner=user_object)
#        item_object_1 = Item.objects.create(list=list_object, text='New item 1')
#        item_object_2 = Item.objects.create(list=list_object, text='New item 2')
#        response = self.client.get('/lists/{}/remove'.format(list_object.pk))
#        
#        self.assertEqual(Item.objects.count(), 2)
#        self.assertEqual(List.objects.count(), 1)
#        self.assertIn(list_object, user_object.list_set.all())
#        self.assertRedirects(response, '/')


