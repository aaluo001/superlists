#------------------------------
# lists.tests.test_forms.test_existing_list_item_form
#------------------------------
# Author: TangJianwei
# Create: 2019-03-10
#------------------------------
from django.test import TestCase
from bs4 import BeautifulSoup

from lists.models import List, Item
from lists.forms  import ExistingListItemForm


class ExistingListItemFormTest(TestCase):
    ''' 对象清单的待办事项表单测试
    '''
    def test_001(self):
        ''' 待办事项输入框及其属性
        '''
        list_object = List.objects.create()
        soup = BeautifulSoup(ExistingListItemForm(for_list=list_object).as_p(), 'html.parser')
        #print(soup)
        item_text = soup.find('input', {'name': 'text'})
        self.assertEqual(item_text['type'], 'text')
        self.assertEqual(item_text['placeholder'], '输入待办事项')
        self.assertEqual(item_text['maxlength'], '32')
        self.assertEqual(item_text['required'], '')
        self.assertEqual(item_text['class'], ['form-control', ])

        
    def test_002(self):
        ''' 不能提交空的待办事项
        '''
        list_object = List.objects.create()
        form = ExistingListItemForm(for_list=list_object, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['待办事项：不能为空！', ])

    
    def test_003(self):
        ''' 提交待办事项的内容不能超过32个字符
        '''
        list_object = List.objects.create()
        form = ExistingListItemForm(for_list=list_object, data={'text': '123456789012345678901234567890123'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['待办事项：不能超过 32 个字符！', ])

        
    def test_004(self):
        ''' 不能提交重复的待办事项
        '''
        list_object = List.objects.create()
        Item.objects.create(list=list_object, text='do me')
        form = ExistingListItemForm(for_list=list_object, data={'text': 'do me'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['您已经提交一个同样的待办事项！', ])
        
        
    def test_005(self):
        ''' 将表单内容保存到数据库
        '''
        list_object = List.objects.create()
        form = ExistingListItemForm(for_list=list_object, data={'text': 'do me'})
        item_object = form.save()
        
        self.assertEqual(item_object, Item.objects.first())
        self.assertEqual(item_object.list, list_object)
        self.assertEqual(item_object.text, 'do me')

