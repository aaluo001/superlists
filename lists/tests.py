from django.test import TestCase
from django.urls import resolve

from lists.views import homePage


class HomePageTest(TestCase):
  
  def test_RootUrlResolveToHomePageView(self):
    vFound = resolve('/')
    self.assertEqual(vFound.func, homePage)

