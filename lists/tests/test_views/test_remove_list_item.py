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
        ''' 未完全删除项目清单
            该清单，以及其他清单项目都未被删除
            页面跳转至清单页面
        '''
        list_object = self.create_list()
        item_object_1 = Item.objects.create(list=list_object, text='New item 1')
        item_object_2 = Item.objects.create(list=list_object, text='New item 2')
        
        response = self.client.get('/lists/{}/remove_item'.format(item_object_1.pk))
        
        self.assertRedirects(response, '/lists/{}/'.format(list_object.pk))
        self.assertIn(item_object_2, list_object.item_set.all())


    def test_002(self):
        ''' 完全删除清单项目
            该清单，以及所有的清单项目都被删除
            页面跳转至我的清单页面
        '''
        list_object = self.create_list()
        item_object = Item.objects.create(list=list_object, text='New item 1')
        
        response = self.client.get('/lists/{}/remove_item'.format(item_object.pk))
        
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)
        self.assertRedirects(response, '/lists/')
    
    
    def test_003(self):
        ''' 未找到要删除的清单项目
            页面跳转至我的清单页面
        '''
        list_object = self.create_list()
        item_object = Item.objects.create(list=list_object, text='New item 1')
        
        response = self.client.get('/lists/{}/remove_item'.format(999))
        
        self.assertRedirects(response, '/lists/')
        self.assertIn(item_object, list_object.item_set.all())

        
    def test_004(self):
        ''' 未登录用户无法删除清单项目
        '''
        other_user_object = User.objects.create(email='other@163.com')
        other_list_object = List.objects.create(owner=other_user_object)
        other_item_object = Item.objects.create(list=other_list_object)

        response = self.client.get('/lists/{}/remove_item'.format(other_item_object.pk))
        
        self.assertRedirects(response, '/')
        self.assertIn(other_item_object, other_list_object.item_set.all())
        
        