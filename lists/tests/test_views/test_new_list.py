#------------------------------
# lists.tests.test_views.test_new_list
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import List, Item
from lists.forms  import ItemForm


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

        
    def test_021(self):
        '''  提交待办事项内容超过32文字时，不会写入数据库
        '''
        self.post_new_list('123456789012345678901234567890123')
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

        
    def test_022(self):
        ''' 提交待办事项内容超过32文字时，返回首页模型
        '''
        response = self.post_new_list('123456789012345678901234567890123')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/index.html')

        
    def test_023(self):
        ''' 提交待办事项内容超过32文字时，返回首页上下文
        '''
        response = self.post_new_list('123456789012345678901234567890123')
        self.assertIsInstance(response.context['form'], ItemForm)

