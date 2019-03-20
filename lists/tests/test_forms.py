#!python
# coding: gbk
#------------------------------
# test_forms.py
#------------------------------
# author: TangJianwei
# update: 2019-03-10
#------------------------------
from django.test import TestCase

from lists.models import List, Item
from lists.forms import (
    ItemForm, ExistingListItemForm,
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR,
)


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="新建一个待办事项"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR, ])

    def test_form_save_handles_saving_to_a_list(self):
        form = ItemForm(data={'text': 'do me'})
        list_object = List.objects.create()
        item_object = form.save(for_list=list_object)
        
        self.assertEqual(item_object, Item.objects.first())
        self.assertEqual(item_object.list, list_object)
        self.assertEqual(item_object.text, 'do me')


class ExistingListItemFormTest(TestCase):
    
    def test_form_renders_item_text_input(self):
        list_object = List.objects.create()
        form = ExistingListItemForm(for_list=list_object)
        self.assertIn('placeholder="新建一个待办事项"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_object = List.objects.create()
        form = ExistingListItemForm(for_list=list_object, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR, ])

    def test_form_validation_for_duplicate_items(self):
        list_object = List.objects.create()
        Item.objects.create(list=list_object, text='do me')
        form = ExistingListItemForm(for_list=list_object, data={'text': 'do me'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR, ])

