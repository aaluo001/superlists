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
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="��������һ�����������"', form.as_p())
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

