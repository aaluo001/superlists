#!python
# coding: gbk
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
    ''' �����嵥�Ĵ������������
    '''
    def test_001(self):
        ''' �������������������
        '''
        list_object = List.objects.create()
        soup = BeautifulSoup(ExistingListItemForm(for_list=list_object).as_p(), 'html.parser')
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
        list_object = List.objects.create()
        form = ExistingListItemForm(for_list=list_object, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['���������Ϊ�գ�', ])

        
    def test_003(self):
        ''' �����ύ�ظ��Ĵ�������
        '''
        list_object = List.objects.create()
        Item.objects.create(list=list_object, text='do me')
        form = ExistingListItemForm(for_list=list_object, data={'text': 'do me'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['���Ѿ��ύһ��ͬ���Ĵ������', ])
        
        
    def test_004(self):
        ''' �������ݱ��浽���ݿ�
        '''
        list_object = List.objects.create()
        form = ExistingListItemForm(for_list=list_object, data={'text': 'do me'})
        item_object = form.save()
        
        self.assertEqual(item_object, Item.objects.first())
        self.assertEqual(item_object.list, list_object)
        self.assertEqual(item_object.text, 'do me')

