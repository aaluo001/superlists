#!python
# coding: gbk
#------------------------------
# lists.forms
#------------------------------
# Author: TangJianwei
# Create: 2019-03-10
#------------------------------
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from lists.models import Item


class ItemForm(ModelForm):
    
    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.fields.TextInput(
                attrs={
                    'placeholder': '���������������',
                    'class': 'form-control',
                    'maxlength': '32',
                }
            )
        }
        error_messages = {
            'text': {
                'required': '�����������ݲ���Ϊ�գ�',
            }
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()


class ExistingListItemForm(ItemForm):
    
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': ['���Ѿ��ύһ��ͬ���Ĵ������',]}
            self._update_errors(e)

    def save(self):
        return ModelForm.save(self)

