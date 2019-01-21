from django.test import TestCase

class SmokeTest(TestCase):
  
  def test_BadMaths(self):
    self.assertEqual(1+1, 4)
