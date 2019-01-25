from django.test import TestCase


class HomePageTest(TestCase):

    def test_UsesHomeTemplate(self):
        vResponse = self.client.get('/')
        self.assertTemplateUsed(vResponse, 'home.html')

