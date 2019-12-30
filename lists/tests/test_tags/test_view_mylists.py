#------------------------------
# lists.tests.test_tags.test_view_mylists
#------------------------------
# Author: TangJianwei
# Create: 2019-12-29
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import List, Item
from lists.templatetags.list_tags import view_mylists


class ViewMylistsTest(TestCase):

    def test_001(self):
        ''' 没有待办事项清单
        '''
        # 其他用户的数据
        other_user = User.objects.create(email='other@163.com')
        other_list = List.objects.create(owner=other_user)
        Item.objects.create(list=other_list, text='other item')

        # 当前用户还没有月账单
        owner = User.objects.create(email='abc@163.com')
        self.assertEqual(len(List.objects.filter(owner=owner)), 0)

        # 没有指定被选中的月账单
        context = view_mylists(owner)
        self.assertEqual(len(context['list_set']), 0)
        self.assertIsNone(context['selected_list'])


    def test_002(self):
        ''' 取得当前用户的月账单数据
        '''
        # 其他用户的数据
        other_user = User.objects.create(email='other@163.com')
        other_list = List.objects.create(owner=other_user)
        Item.objects.create(list=other_list, text='other item')

        # 当前用户的月账单
        owner = User.objects.create(email='abc@163.com')
        my_list_1 = List.objects.create(owner=owner)
        my_list_2 = List.objects.create(owner=owner)
        Item.objects.create(list=my_list_1, text='my text 1')
        Item.objects.create(list=my_list_2, text='my text 2')

        # 指定了被选中的月账单
        context = view_mylists(owner, my_list_2)
        list_set = context['list_set']
        self.assertEqual(len(list_set), 2)
        self.assertIn(my_list_1, list_set)
        self.assertIn(my_list_2, list_set)
        self.assertEqual(context['selected_list'], my_list_2)

