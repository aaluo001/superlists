#!python
# coding: gbk
#------------------------------
# forms.py
#------------------------------
# author: TangJianwei
# update: 2019-03-10
#------------------------------
from django import forms
from django.forms import ModelForm
from lists.models import Item


EMPTY_ITEM_ERROR = '�������ύһ���յĴ������'


class ItemForm(ModelForm):
    
    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': '��������һ�����������',
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'text': {
                'required': EMPTY_ITEM_ERROR,
            }
        }




