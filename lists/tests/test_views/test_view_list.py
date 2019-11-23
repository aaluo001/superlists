#------------------------------
# lists.tests.test_views.test_view_list
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
from unittest.mock import patch, call

from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import List, Item
from lists.forms  import ItemForm, ExistingListItemForm


class ViewListTestForRequestGET(TestCase):
    ''' 显示清单项目测试
    '''
    def get_view_list(self, list_object):
        return self.client.get(list_object.get_absolute_url())
    
    
    def test_001(self):
        ''' 清单项目显示页面
        '''
        response = self.get_view_list(List.objects.create())
        self.assertTemplateUsed(response, 'lists/list.html')

        
    def test_002(self):
        ''' 清单项目显示上下文(匿名用户)
        '''
        other_list_object = List.objects.create()       ## 不会取到错误的清单
        list_object = List.objects.create()
        
        response = self.get_view_list(list_object)
        
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertEqual(response.context['list'], list_object)
        self.assertIsNone(response.context['list_set'])

        
    def test_003(self):
        ''' 清单项目显示上下文(登录用户)
        '''
        other_list_object = List.objects.create()       ## 不会取到错误的清单
        user_object = User.objects.create(email='abc@163.com')
        self.client.force_login(user_object)
        list_object = List.objects.create(owner=user_object)
        Item.objects.create(list=list_object, text='new item')
        
        response = self.get_view_list(list_object)
        
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertEqual(response.context['list'], list_object)
        
        list_set = response.context['list_set']
        self.assertEqual(len(list_set), 1)
        self.assertEqual(list_set[0], list_object)


    @patch('lists.views.messages')
    def test_011(self, mock_messages):
        ''' 无法取得未保存到数据库的清单
        '''
        # 未保存到数据库的清单
        list_object = List()
        list_object.id = 99
        
        response = self.get_view_list(list_object)

        self.assertEqual(
            mock_messages.error.call_args,
            call(response.wsgi_request, '没有找到该清单，或该清单已被删除！')
        )
        self.assertRedirects(response, '/')

        
    def test_012(self):
        ''' 匿名用户无法取得已指定拥有者的清单
        '''
        user_object = User.objects.create(email='abc@163.com')
        # 已指定拥有者的清单
        list_object = List.objects.create(owner=user_object)
        # 未登录用户
        # self.client.force_login(user_object)
        response = self.get_view_list(list_object)
        self.assertRedirects(response, '/')

        
    def test_013(self):
        ''' 登录用户无法取得未指定拥有者的清单
        '''
        user_object = User.objects.create(email='abc@163.com')
        # 未指定拥有者的清单
        list_object = List.objects.create()
        self.client.force_login(user_object)
        response = self.get_view_list(list_object)
        self.assertRedirects(response, '/')

        
        
        
class ViewListTestForRequestPOST(TestCase):
    ''' 添加清单项目测试
    '''
    def post_item_text_input(self, list_object, item_text):
        return self.client.post(
            list_object.get_absolute_url(), \
            data={'text': item_text} \
        )


    def test_001(self):
        ''' 提交的待办事项内容可以保存到数据库
        '''
        other_list_object = List.objects.create()   ## 不会取到错误的清单项目
        list_object = List.objects.create()

        self.post_item_text_input(list_object, 'A new item 1')
        self.post_item_text_input(list_object, 'A new item 2')

        self.assertEqual(Item.objects.count(), 2)

        item_object_arr = Item.objects.all()
        self.assertEqual(item_object_arr[0].text, 'A new item 1')
        self.assertEqual(item_object_arr[1].text, 'A new item 2')
        self.assertEqual(item_object_arr[0].list, list_object)
        self.assertEqual(item_object_arr[1].list, list_object)

        
    def test_002(self):
        ''' 处理完了后页面跳转到清单项目显示
        '''
        other_list_object = List.objects.create()
        list_object = List.objects.create()
        response = self.post_item_text_input(list_object, 'A new item')
        self.assertRedirects(response, list_object.get_absolute_url())


    @patch('lists.views.messages')
    def test_011(self, mock_messages):
        ''' 无法取得未保存到数据库的清单
        '''
        # 未保存到数据库的清单
        list_object = List()
        list_object.id = 99
        
        response = self.post_item_text_input(list_object, 'A New item')

        self.assertEqual(
            mock_messages.error.call_args,
            call(response.wsgi_request, '没有找到该清单，或该清单已被删除！')
        )
        self.assertRedirects(response, '/')

        
    def test_021(self):
        ''' 提交空的待办事项时，不会保存到数据库
        '''
        self.post_item_text_input(List.objects.create(), '')
        self.assertEqual(Item.objects.count(), 0)

    def test_022(self):
        '''  提交待办事项内容超过32文字时，不会保存到数据库
        '''
        self.post_item_text_input(List.objects.create(), '123456789012345678901234567890123')
        self.assertEqual(Item.objects.count(), 0)

    def test_023(self):
        ''' 提交重复的待办事项时，不会保存到数据库
        '''
        list_object = List.objects.create()
        Item.objects.create(list=list_object, text='do me')
        # 提交重复的待办事项
        response = self.post_item_text_input(list_object, 'do me')
        self.assertEqual(Item.objects.count(), 1)


    def test_031(self):
        ''' 提交出错时，显示清单项目页面
        '''
        response = self.post_item_text_input(List.objects.create(), '')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_032(self):
        ''' 提交出错时，清单项目显示上下文
        '''
        list_object = List.objects.create()
        response = self.post_item_text_input(list_object, '')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertEqual(response.context['list'], list_object)
        self.assertIsNone(response.context['list_set'])

    def test_033(self):
        ''' 如果时登录用户，提交出错时，仍可以取得我的清单
        '''
        other_list_object = List.objects.create()
        Item.objects.create(list=other_list_object, text='Other item')
        
        user_object = User.objects.create(email='abc@163.com')
        self.client.force_login(user_object)

        ## 新建清单
        list_object_1 = List.objects.create(owner=user_object)
        Item.objects.create(list=list_object_1, text='New item 1')
        list_object_2 = List.objects.create(owner=user_object)
        Item.objects.create(list=list_object_2, text='New item 2')

        # 提交出错(提交空的待办事项)
        response = self.post_item_text_input(list_object_1, '')

        list_set = response.context['list_set']
        self.assertEqual(len(list_set), 2)
        self.assertIn(list_object_1, list_set)
        self.assertIn(list_object_2, list_set)
        self.assertNotIn(other_list_object, list_set)

