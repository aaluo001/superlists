#!python
# coding: utf-8
#------------------------------
# lists.tests.test_views.test_my_lists
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import List


class MyListsTest(TestCase):

    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email='abc@163.com')
        response = self.client.get('/lists/users/abc@163.com/')
        self.assertTemplateUsed(response, 'my_lists.html')


    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@163.com')
        user_object = User.objects.create(email='abc@163.com')
        response = self.client.get('/lists/users/abc@163.com/')
        self.assertEqual(response.context['owner'], user_object)

