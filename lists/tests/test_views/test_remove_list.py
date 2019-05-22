#!python
# coding: utf-8
#------------------------------
# lists.tests.test_views
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import List, Item
from lists.forms  import ItemForm, ExistingListItemForm


class HomePageTest(TestCase):
    ''' 首页测试
    '''
    def test_001(self):
        ''' 首页显示页面
        '''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/index.html')

    def test_002(self):
        ''' 首页显示上下文
        '''
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):
    ''' 新建表单测试
    '''
    def post_new_list(self, item_text='A new list item'):
        return self.client.post('/lists/new', data={'text': item_text})

    
    def test_001(self):
        ''' 新建表单(匿名用户)
        '''
        self.post_new_list()

        list_object = List.objects.first()
        self.assertIsNone(list_object.owner)
        self.assertEqual(list_object.item_set.count(), 1)
        
        item_object = list_object.item_set.first()
        self.assertEqual(item_object.text, 'A new list item')

        
    def test_002(self):
        ''' 新建表单(登录用户)
        '''
        user_object = User.objects.create(email='abc@163.com')
        self.client.force_login(user_object)
        self.post_new_list()
        
        list_object = List.objects.first()
        self.assertEqual(list_object.owner, user_object)

        
    def test_003(self):
        ''' 新建清单后页面跳转到显示清单页面
        '''
        response = self.post_new_list()
        list_object = List.objects.first()
        self.assertRedirects(response, list_object.get_absolute_url())


    def test_011(self):
        ''' 提交空的待办事项时，不会写入数据库
        '''
        self.post_new_list('')
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

        
    def test_012(self):
        ''' 提交空的待办事项时，返回首页模型
        '''
        response = self.post_new_list('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/index.html')

        
    def test_013(self):
        ''' 提交空的待办事项时，返回首页上下文
        '''
        response = self.post_new_list('')
        self.assertIsInstance(response.context['form'], ItemForm)


    def test_014(self):
        ''' 提交空的待办事项时，返回错误消息
        '''
        response = self.post_new_list('')
        self.assertContains(response, '待办事项内容不能为空！')



class ViewListTest(TestCase):
    ''' 显示和添加清单项目测试
    '''
    def get_view_list(self, list_object):
        return self.client.get(list_object.get_absolute_url())

    def post_item_text_input(self, list_object, item_text):
        return self.client.post(
            list_object.get_absolute_url(), \
            data={'text': item_text} \
        )
    
    
    def test_001(self):
        ''' 清单项目显示页面
        '''
        response = self.get_view_list(List.objects.create())
        self.assertTemplateUsed(response, 'lists/list.html')

        
    def test_002(self):
        ''' 清单项目显示上下文
        '''
        other_list_object = List.objects.create()       ## 不会取到错误的清单
        list_object = List.objects.create()
        response = self.get_view_list(list_object)
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertEqual(response.context['list'], list_object)


    def test_003(self):
        ''' 正确取得该清单项目，而不会取到其他清单的项目
        '''
        list_object = List.objects.create()
        Item.objects.create(text='Itemey 1', list=list_object)
        Item.objects.create(text='Itemey 2', list=list_object)
        
        ## 不会取到错误的清单项目
        other_list_object = List.objects.create()
        Item.objects.create(text='Other list item 1', list=other_list_object)
        Item.objects.create(text='Other list item 2', list=other_list_object)
        
        response = self.get_view_list(list_object)
        
        self.assertContains(response, 'Itemey 1')
        self.assertContains(response, 'Itemey 2')
        self.assertNotContains(response, 'Other list item 1')
        self.assertNotContains(response, 'Other list item 2')

    
    def test_004(self):
        ''' 匿名用户不能取得已有拥有者的清单
        '''
        user_object = User.objects.create(email='abc@163.com')
        list_object = List.objects.create(owner=user_object)
        self.get_view_list(list_object)
        self.fail('Finished the test!')
    
    
    def test_011(self):
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

        
    def test_012(self):
        ''' 处理完了后页面跳转到清单项目显示
        '''
        other_list_object = List.objects.create()
        list_object = List.objects.create()
        response = self.post_item_text_input(list_object, 'A new item')
        self.assertRedirects(response, list_object.get_absolute_url())


    def test_021(self):
        ''' 提交空的待办事项不会保存到数据库
        '''
        self.post_item_text_input(List.objects.create(), '')
        self.assertEqual(Item.objects.count(), 0)

        
    def test_022(self):
        ''' 提交空的待办事项后，清单项目显示页面
        '''
        response = self.post_item_text_input(List.objects.create(), '')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')
        
        
    def test_023(self):
        ''' 提交空的待办事项后，清单项目显示上下文
        '''
        list_object = List.objects.create()
        response = self.post_item_text_input(list_object, '')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertEqual(response.context['list'], list_object)


    def test_024(self):
        ''' 提交空的待办事项后，错误消息
        '''
        response = self.post_item_text_input(List.objects.create(), '')
        self.assertContains(response, '待办事项内容不能为空！')


    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        ''' 提交重复的待办事项，数据库不会更新
            错误消息和清单项目显示页面
        '''
        list_object = List.objects.create()
        Item.objects.create(list=list_object, text='do me')
        
        # 提交重复的待办事项
        response = self.post_item_text_input(list_object, 'do me')
        
        self.assertEqual(Item.objects.count(), 1)
        self.assertContains(response, '您已经提交一个同样的待办事项！')
        self.assertTemplateUsed(response, 'lists/list.html')


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

