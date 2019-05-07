#!python
# coding: gbk
#------------------------------
# test_models.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from django.test import TestCase
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import Item
from lists.models import List


class ItemModelTest(TestCase):
    
    def test_default_text(self):
        item_object = Item()
        self.assertEqual(item_object.text, '')
    
    def test_item_is_related_to_list(self):
        list_object = List.objects.create()
        #item_object = Item(list=list_object, text='do me')
        item_object = Item()
        item_object.list = list_object
        item_object.save()
        self.assertIn(item_object, list_object.item_set.all())


#    def test_saving_and_retrieving_items(self):
#        list_object = List()
#        list_object.save()
#        
#        item_object_1 = Item()
#        item_object_1.text = 'The first (ever) list item'
#        item_object_1.list = list_object
#        item_object_1.save()
#        
#        item_object_2 = Item()
#        item_object_2.text = 'Item the second'
#        item_object_2.list = list_object
#        item_object_2.save()
#        
#        saved_items = Item.objects.all()
#        self.assertEqual(saved_items.count(), 2)
#        self.assertEqual(saved_items[0].text, 'The first (ever) list item')
#        self.assertEqual(saved_items[0].list, list_object)
#        self.assertEqual(saved_items[1].text, 'Item the second')
#        self.assertEqual(saved_items[1].list, list_object)


    def test_cannot_save_empty_list_items(self):
        list_object = List.objects.create()
        item_object = Item(list=list_object, text='')
        with self.assertRaises(ValidationError):
            item_object.save()
            item_object.full_clean()

    def test_dupicate_items_are_invalid(self):
        list_object = List.objects.create()
        Item.objects.create(list=list_object, text='do me')
        with self.assertRaises(ValidationError):
            item_object = Item(list=list_object, text='do me')
            item_object.full_clean()
            #item_object.save()

    def test_CAN_save_same_items_to_different_lists(self):
        list_object_1 = List.objects.create()
        list_object_2 = List.objects.create()
        Item.objects.create(list=list_object_1, text='do me')
        item_object = Item(list=list_object_2, text='do me')
        item_object.full_clean()    # 不会出现异常


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_object = List.objects.create()
        self.assertEqual( \
            list_object.get_absolute_url(), \
            '/lists/{}/'.format(list_object.id) \
        )

    def test_lists_can_have_owners(self):
        user_object = User.objects.create(email='abc@163.com')
        list_object = List.objects.create(owner=user_object)
        self.assertIn(list_object, user_object.list_set.all())

