from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import homePage


class HomePageTest(TestCase):
  
  def test_RootUrlResolvesToHomePageView(self):
    vFound = resolve('/')
    self.assertEqual(vFound.func, homePage)


  def test_HomePageReturnsCorrectHtml(self):
    vRequest = HttpRequest()
    vResponse = homePage(vRequest)
    vHtml = vResponse.content.decode('UTF8')
    
    self.assertTrue(vHtml.startswith('<html>'))
    self.assertIn('<title>To-Do lists</title>', vHtml)
    self.assertTrue(vHtml.endswith('</html>'))

