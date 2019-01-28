from django.test import TestCase


class HomePageTest(TestCase):

    def test_UsesHomeTemplate(self):
        vResponse = self.client.get('/')
        self.assertTemplateUsed(vResponse, 'home.html')

    def test_CanSaveAPostRequest(self):
        vResponse = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', vResponse.content.decode())
        self.assertTemplateUsed(vResponse, 'home.html')

