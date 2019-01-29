from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):

    def test_UsesHomeTemplate(self):
        vResponse = self.client.get('/')
        self.assertTemplateUsed(vResponse, 'home.html')


    def test_CanSaveAPostRequest(self):
        vResponse = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        vNewItem = Item.objects.first()
        self.assertEqual(vNewItem.text, 'A new list item')


    def test_RedirectsAfterPost(self):
        vResponse = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(vResponse.status_code, 302)
        self.assertEqual(vResponse['location'], '/')


    def test_DisplaysAllListItems(self):
        Item.objects.create(text='Itemey 1')
        Item.objects.create(text='Itemey 2')
        
        vResponse = self.client.get('/')
        
        self.assertIn('Itemey 1', vResponse.content.decode())
        self.assertIn('Itemey 2', vResponse.content.decode())


class ItemModelTests(TestCase):
    
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

