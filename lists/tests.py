from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):

    def test_UsesHomeTemplate(self):
        vResponse = self.client.get('/')
        self.assertTemplateUsed(vResponse, 'home.html')

    def test_OnlySavesItemsWhenNecessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class NewListTest(TestCase):

    def test_CanSaveAPostRequest(self):
        vResponse = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        vNewItem = Item.objects.first()
        self.assertEqual(vNewItem.text, 'A new list item')

    def test_RedirectsAfterPost(self):
        vResponse = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(vResponse, '/lists/the-only-list/')



class ViewListTest(TestCase):

    def test_UsesListTemplate(self):
        vResponse = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(vResponse, 'list.html')

    def test_DisplaysAllListItems(self):
        Item.objects.create(text='Itemey 1')
        Item.objects.create(text='Itemey 2')
        
        vResponse = self.client.get('/lists/the-only-list/')
        
        self.assertContains(vResponse, 'Itemey 1')
        self.assertContains(vResponse, 'Itemey 2')


class ItemModelTest(TestCase):
    
    def test_SavingAndRetrievingItems(self):
        vFirstItem = Item()
        vFirstItem.text = 'The first (ever) list item'
        vFirstItem.save()
        
        vSecondItem = Item()
        vSecondItem.text = 'Item the second'
        vSecondItem.save()
        
        vSaveItems = Item.objects.all()
        self.assertEqual(vSaveItems.count(), 2)
        self.assertEqual(vSaveItems[0].text, 'The first (ever) list item')
        self.assertEqual(vSaveItems[1].text, 'Item the second')

