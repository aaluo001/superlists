from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):

    def test_UsesHomeTemplate(self):
        vResponse = self.client.get('/')
        self.assertTemplateUsed(vResponse, 'home.html')

    def test_CanSaveAPostRequest(self):
        vResponse = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', vResponse.content.decode())
        self.assertTemplateUsed(vResponse, 'home.html')


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

