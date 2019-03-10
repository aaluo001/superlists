#!python
# coding: gbk
#------------------------------
# test_views.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from django.test import TestCase
from lists.models import Item
from lists.models import List
from lists.forms import ItemForm


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        item_object = Item.objects.first()
        self.assertEqual(item_object.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        list_object = List.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(list_object.id))

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, "您不能提交一个空的待办事项！")

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


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

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list_object = List.objects.create()
        list_object = List.objects.create()

        self.client.post(
            '/lists/{}/'.format(list_object.id), \
            data={'text': 'A new item for an existing list'} \
        )

        self.assertEqual(Item.objects.count(), 1)
        item_object = Item.objects.first()
        self.assertEqual(item_object.text, 'A new item for an existing list')
        self.assertEqual(item_object.list, list_object)

    def test_POST_redirects_to_list_view(self):
        other_list_object = List.objects.create()
        list_object = List.objects.create()

        response = self.client.post(
            '/lists/{}/'.format(list_object.id), \
            data={'text': 'A new item for an existing list'} \
        )

        self.assertRedirects(response, '/lists/{}/'.format(list_object.id))

    def test_validation_errors_end_up_on_list_page(self):
        list_object = List.objects.create()
        response = self.client.post(
            '/lists/{}/'.format(list_object.id), \
            data={'text': ''} \
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertContains(response, "您不能提交一个空的待办事项！")

