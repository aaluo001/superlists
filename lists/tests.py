#!python
# coding: gbk
#------------------------------
# tests.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from django.test import TestCase
from lists.models import Item
from lists.models import List


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class NewListTest(TestCase):

    def test_can_save_a_post_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        item_object = Item.objects.first()
        self.assertEqual(item_object.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        list_object = List.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(list_object.id))


class ViewListTest(TestCase):

    def test_uses_list_template(self):
        list_object = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_object.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        list_object = List.objects.create()
        Item.objects.create(text='Itemey 1', list=list_object)
        Item.objects.create(text='Itemey 2', list=list_object)
        
        other_list_object = List.objects.create()
        Item.objects.create(text='Other list item 1', list=other_list_object)
        Item.objects.create(text='Other list item 2', list=other_list_object)
        
        response = self.client.get('/lists/{}/'.format(list_object.id))
        
        self.assertContains(response, 'Itemey 1')
        self.assertContains(response, 'Itemey 2')
        self.assertNotContains(response, 'Other list item 1')
        self.assertNotContains(response, 'Other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list_object = List.objects.create()
        list_object = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_object.id))
        self.assertEqual(response.context['list'], list_object)


class AddItemTest(TestCase):
    
    def test_can_save_a_post_request_to_an_existing_list(self):
        other_list_object = List.objects.create()
        list_object = List.objects.create()
        
        response = self.client.post( \
            '/lists/{}/add_item'.format(list_object.id), \
            data={'item_text': 'A new list item for an existing list'} \
        )
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item for an existing list')
        self.assertEqual(new_item.list, list_object)

    def test_redirects_after_post(self):
        other_list_object = List.objects.create()
        list_object = List.objects.create()
        
        response = self.client.post( \
            '/lists/{}/add_item'.format(list_object.id), \
            data={'item_text': 'A new list item for an existing list'} \
        )

        self.assertRedirects(response, '/lists/{}/'.format(list_object.id))


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

