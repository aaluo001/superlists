#------------------------------
# lists.tests.test_views.test_home_page
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import List, Item
from lists.forms import ItemForm


class HomePageTest(TestCase):
    ''' 首页测试
    '''
    def test_001(self):
        ''' 迁移到index.html页面
        '''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/index.html')


    def test_002(self):
        ''' 返回上下文form=ItemForm()
        '''
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


    # def test_003(self):
    #     ''' 如果是匿名用户，即使新建了清单，返回上下文中的list_set也是空([])
    #     '''
    #     list_object = List.objects.create()
    #     Item.objects.create(list=list_object, text='new item 1')
    #     response = self.client.get('/')
    #     self.assertIsNone(response.context['list_set'])


    # def test_004(self):
    #     ''' 如果是登录用户，没有新建清单时，返回上下文中的list_set是空([])
    #     '''
    #     user_object = User.objects.create(email='abc@163.com')
    #     self.client.force_login(user_object)

    #     ## 没有新建清单，直接访问首页
    #     response = self.client.get('/')

    #     list_set = response.context['list_set']
    #     self.assertEqual(len(list_set), 0)


    def test_005(self):
        ''' 上下文 list_set=List.objects.filter(owner=myself)
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

        response = self.client.get('/')

        list_set = response.context['list_set']
        self.assertEqual(len(list_set), 2)
        self.assertIn(list_object_1, list_set)
        self.assertIn(list_object_2, list_set)
        self.assertNotIn(other_list_object, list_set)

