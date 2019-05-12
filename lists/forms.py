#!python
# coding: gbk
#------------------------------
# lists.forms.py
#------------------------------
# author: TangJianwei
# update: 2019-03-10
#------------------------------
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from lists.models import Item


TEXT_PLACEHOLDER        = '���������������'
TEXT_LENGTH_ERROR       = '�����������ݲ��ܳ���64���֣�'
TEXT_EMPTY_ERROR        = '�����������ݲ���Ϊ�գ�'
TEXT_DUPLICATE_ERROR    = '���Ѿ��ύһ��ͬ���Ĵ������'


class ItemForm(ModelForm):
    
    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': TEXT_PLACEHOLDER,
                'class': 'form-control',
            })
        }
        error_messages = {
            'text': {
                'required': TEXT_EMPTY_ERROR,
            }
        }


    def clean_text(self):
        cleaned_data = self.cleaned_data['text']
        if (len(cleaned_data) > 64):
            raise ValidationError(TEXT_LENGTH_ERROR)
        return cleaned_data

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
            e.error_dict = {'text': [TEXT_DUPLICATE_ERROR,]}
            self._update_errors(e)

    def save(self):
        return ModelForm.save(self)

