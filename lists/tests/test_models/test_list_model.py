#------------------------------
# lists.tests.test_models.test_list_model
#------------------------------
# Author: TangJianwei
# Create: 2019-02-25
#------------------------------
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.models import List, Item


class ListModelTest(TestCase):
    ''' 清单模型测试
    '''
    def test_001(self):
        ''' 取得清单的URL链接
        '''
        list_object = List.objects.create()
        self.assertEqual( \
            list_object.get_absolute_url(), \
            '/lists/{}/'.format(list_object.id) \
        )


    def test_002(self):
        ''' 可以指定清单的拥有者
        '''
        user_object = User.objects.create(email='abc@163.com')
        list_object = List.objects.create(owner=user_object)
        self.assertIn(list_object, user_object.list_set.all())


    def test_003(self):
        ''' 可以不指定清单的拥有者
        '''
        # 新建一条清单数据，清单的拥有者是NULL
        List.objects.create()
        self.assertIsNone(List.objects.first().owner)
        
        # 下面会出现异常，因为owner字段没有指定blank=True
        with self.assertRaises(ValidationError):
            list_object = List()
            list_object.full_clean()
            #list_object.save()


    def test_004(self):
        ''' 清单的标题是第一条待办事项
        '''
        list_object = List.objects.create()
        Item.objects.create(list=list_object, text='first item')
        Item.objects.create(list=list_object, text='second item')
        self.assertEqual(list_object.name, 'first item')

