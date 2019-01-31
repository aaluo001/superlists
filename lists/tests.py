from django.test import TestCase
from lists.models import Item
from lists.models import List


class HomePageTest(TestCase):

    def test_UsesHomeTemplate(self):
        vResponse = self.client.get('/')
        self.assertTemplateUsed(vResponse, 'home.html')


class NewListTest(TestCase):

    def test_CanSaveAPostRequest(self):
        vResponse = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        vNewItem = Item.objects.first()
        self.assertEqual(vNewItem.text, 'A new list item')

    def test_RedirectsAfterPost(self):
        vResponse = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        vNewList = List.objects.first()
        self.assertRedirects(vResponse, '/lists/{}/'.format(vNewList.id))



class ViewListTest(TestCase):

    def test_UsesListTemplate(self):
        vList = List.objects.create()
        vResponse = self.client.get('/lists/{}/'.format(vList.id))
        self.assertTemplateUsed(vResponse, 'list.html')

    def test_DisplaysOnlyItemsForThatList(self):
        vList = List.objects.create()
        Item.objects.create(text='Itemey 1', list=vList)
        Item.objects.create(text='Itemey 2', list=vList)
        
        vOtherList = List.objects.create()
        Item.objects.create(text='Other list item 1', list=vOtherList)
        Item.objects.create(text='Other list item 2', list=vOtherList)
        
        vResponse = self.client.get('/lists/{}/'.format(vList.id))
        
        self.assertContains(vResponse, 'Itemey 1')
        self.assertContains(vResponse, 'Itemey 2')
        self.assertNotContains(vResponse, 'Other list item 1')
        self.assertNotContains(vResponse, 'Other list item 2')

    def test_PassesCorrectListToTemplate(self):
        vWorngList = List.objects.create()
        vList = List.objects.create()
        vResponse = self.client.get('/lists/{}/'.format(vList.id))
        self.assertEqual(vResponse.context['list'], vList)


class AddItemTest(TestCase):
    
    def test_CanSaveAPostRequestToAnExistingList(self):
        vWorngList = List.objects.create()
        vList = List.objects.create()
        
        vResponse = self.client.post( \
            '/lists/{}/add_item'.format(vList.id), \
            data={'item_text': 'A new list item for an existing list'} \
        )
        
        self.assertEqual(Item.objects.count(), 1)
        vNewItem = Item.objects.first()
        self.assertEqual(vNewItem.text, 'A new list item for an existing list')
        self.assertEqual(vNewItem.list, vList)

    def test_RedirectsAfterPost(self):
        vWorngList = List.objects.create()
        vList = List.objects.create()
        
        vResponse = self.client.post( \
            '/lists/{}/add_item'.format(vList.id), \
            data={'item_text': 'A new list item for an existing list'} \
        )

        self.assertRedirects(vResponse, '/lists/{}/'.format(vList.id))


class ListAndItemModelTest(TestCase):
    
    def test_SavingAndRetrievingItems(self):
        vList = List()
        vList.save()
        
        vFirstItem = Item()
        vFirstItem.text = 'The first (ever) list item'
        vFirstItem.list = vList
        vFirstItem.save()
        
        vSecondItem = Item()
        vSecondItem.text = 'Item the second'
        vSecondItem.list = vList
        vSecondItem.save()
        
        vSaveItems = Item.objects.all()
        self.assertEqual(vSaveItems.count(), 2)
        self.assertEqual(vSaveItems[0].text, 'The first (ever) list item')
        self.assertEqual(vSaveItems[0].list, vList)
        self.assertEqual(vSaveItems[1].text, 'Item the second')
        self.assertEqual(vSaveItems[1].list, vList)

