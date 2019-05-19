#!python
# coding: gbk
#------------------------------
# lists.tests.test_models
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import List, Item


class ItemModelTest(TestCase):
    ''' 待办事项模型测试
    '''
    def test_001(self):
        ''' 待办事项内容(text)默认是空
        '''
        item_object = Item()
        self.assertEqual(item_object.text, '')


    def test_002(self):
        ''' Item的外键是List
        '''
        list_object = List.objects.create()
        item_object = Item()
        item_object.list = list_object
        item_object.save()
        self.assertIn(item_object, list_object.item_set.all())


    def test_003(self):
        ''' 待办事项的内容不能为空
        '''
        list_object = List.objects.create()
        item_object = Item(list=list_object, text='')
        
        with self.assertRaises(ValidationError):
            item_object.full_clean()
            #item_object.save()


    def test_004(self):
        ''' 对于同一List，待办事项的内容不能重复
        '''
        list_object = List.objects.create()
        Item.objects.create(list=list_object, text='do me')
        
        with self.assertRaises(ValidationError):
            item_object = Item(list=list_object, text='do me')
            item_object.full_clean()
            #item_object.save()


    def test_005(self):
        ''' 对于不同的List，待办事项的内容可以重复
        '''
        list_object_1 = List.objects.create()
        list_object_2 = List.objects.create()
        Item.objects.create(list=list_object_1, text='do me')
        
        item_object = Item(list=list_object_2, text='do me')
        item_object.full_clean()    ## 不会出现异常


class ListModelTest(TestCase):
    ''' 清单模型测试
    '''
    def test_001(self):
        ''' 取得清单的URL链接
        '''
        list_object = List.objects.create()
        self.assertEqual( \
            list_object.get_absolute_url(), \
            '/lists/{}/'.format(list_object.id) \
        )


    def test_002(self):
        ''' 可以指定清单的拥有者
        '''
        user_object = User.objects.create(email='abc@163.com')
        list_object = List.objects.create(owner=user_object)
        self.assertIn(list_object, user_object.list_set.all())


    def test_003(self):
        ''' 可以不指定清单的拥有者
        '''
        # 新建一条清单数据，清单的拥有者是NULL
        List.objects.create()
        self.assertIsNone(List.objects.first().owner)
        
        # 下面会出现异常，因为owner字段没有指定blank=True
        with self.assertRaises(ValidationError):
            list_object = List()
            list_object.full_clean()
            #list_object.save()


    def test_004(self):
        ''' 清单的标题是第一条待办事项
        '''
        list_object = List.objects.create()
        Item.objects.create(list=list_object, text='first item')
        Item.objects.create(list=list_object, text='second item')
        self.assertEqual(list_object.name, 'first item')

