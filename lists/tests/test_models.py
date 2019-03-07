#!python
# coding: gbk
#------------------------------
# test_models.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from django.test import TestCase
from lists.models import Item
from lists.models import List


class ListAndItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        list_object = List()
        list_object.save()
        
        item_object_1 = Item()
        item_object_1.text = 'The first (ever) list item'
        item_object_1.list = list_object
        item_object_1.save()
        
        item_object_2 = Item()
        item_object_2.text = 'Item the second'
        item_object_2.list = list_object
        item_object_2.save()
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, 'The first (ever) list item')
        self.assertEqual(saved_items[0].list, list_object)
        self.assertEqual(saved_items[1].text, 'Item the second')
        self.assertEqual(saved_items[1].list, list_object)

