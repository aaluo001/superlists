#------------------------------
# lists.tests.test_models.test_item_model
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

