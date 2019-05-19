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
    ''' ��������ģ�Ͳ���
    '''
    def test_001(self):
        ''' ������������(text)Ĭ���ǿ�
        '''
        item_object = Item()
        self.assertEqual(item_object.text, '')


    def test_002(self):
        ''' Item�������List
        '''
        list_object = List.objects.create()
        item_object = Item()
        item_object.list = list_object
        item_object.save()
        self.assertIn(item_object, list_object.item_set.all())


    def test_003(self):
        ''' ������������ݲ���Ϊ��
        '''
        list_object = List.objects.create()
        item_object = Item(list=list_object, text='')
        
        with self.assertRaises(ValidationError):
            item_object.full_clean()
            #item_object.save()


    def test_004(self):
        ''' ����ͬһList��������������ݲ����ظ�
        '''
        list_object = List.objects.create()
        Item.objects.create(list=list_object, text='do me')
        
        with self.assertRaises(ValidationError):
            item_object = Item(list=list_object, text='do me')
            item_object.full_clean()
            #item_object.save()


    def test_005(self):
        ''' ���ڲ�ͬ��List��������������ݿ����ظ�
        '''
        list_object_1 = List.objects.create()
        list_object_2 = List.objects.create()
        Item.objects.create(list=list_object_1, text='do me')
        
        item_object = Item(list=list_object_2, text='do me')
        item_object.full_clean()    ## ��������쳣


class ListModelTest(TestCase):
    ''' �嵥ģ�Ͳ���
    '''
    def test_001(self):
        ''' ȡ���嵥��URL����
        '''
        list_object = List.objects.create()
        self.assertEqual( \
            list_object.get_absolute_url(), \
            '/lists/{}/'.format(list_object.id) \
        )


    def test_002(self):
        ''' ����ָ���嵥��ӵ����
        '''
        user_object = User.objects.create(email='abc@163.com')
        list_object = List.objects.create(owner=user_object)
        self.assertIn(list_object, user_object.list_set.all())


    def test_003(self):
        ''' ���Բ�ָ���嵥��ӵ����
        '''
        # �½�һ���嵥���ݣ��嵥��ӵ������NULL
        List.objects.create()
        self.assertIsNone(List.objects.first().owner)
        
        # ���������쳣����Ϊowner�ֶ�û��ָ��blank=True
        with self.assertRaises(ValidationError):
            list_object = List()
            list_object.full_clean()
            #list_object.save()


    def test_004(self):
        ''' �嵥�ı����ǵ�һ����������
        '''
        list_object = List.objects.create()
        Item.objects.create(list=list_object, text='first item')
        Item.objects.create(list=list_object, text='second item')
        self.assertEqual(list_object.name, 'first item')

