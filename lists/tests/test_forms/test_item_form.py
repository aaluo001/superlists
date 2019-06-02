#!python
# coding: gbk
#------------------------------
# lists.tests.test_forms.test_item_form
#------------------------------
# Author: TangJianwei
# Create: 2019-03-10
#------------------------------
from django.test import TestCase
from bs4 import BeautifulSoup

from lists.models import List, Item
from lists.forms  import ItemForm


class ItemFormTest(TestCase):
    ''' �½��嵥�Ĵ������������
    '''
    def test_001(self):
        ''' �������������������
        '''
        soup = BeautifulSoup(ItemForm().as_p(), 'html.parser')
        #print(soup)
        item_text = soup.find('input', {'name': 'text'})
        self.assertEqual(item_text['type'], 'text')
        self.assertEqual(item_text['placeholder'], '�����������')
        self.assertEqual(item_text['maxlength'], '32')
        self.assertEqual(item_text['required'], '')
        self.assertEqual(item_text['class'], ['form-control', ])


    def test_002(self):
        ''' �����ύ�յĴ�������
        '''
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['���������Ϊ�գ�', ])

    
    def test_003(self):
        ''' �ύ������������ݲ��ܳ���32����
        '''
        form = ItemForm(data={'text': '123456789012345678901234567890123'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['������������ݲ��ܳ���32���֣�', ])
    
    
    def test_004(self):
        ''' �������ݱ��浽���ݿ�
        '''
        form = ItemForm(data={'text': 'do me'})
        list_object = List.objects.create()
        item_object = form.save(for_list=list_object)
        
        self.assertEqual(item_object, Item.objects.first())
        self.assertEqual(item_object.list, list_object)
        self.assertEqual(item_object.text, 'do me')

