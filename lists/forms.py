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


EMPTY_ITEM_ERROR = '您不能提交一个空的待办事项！'
DUPLICATE_ITEM_ERROR = '您已经有一条同样的待办事项！'


class ItemForm(ModelForm):
    
    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': '新建一个待办事项',
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'text': {
                'required': EMPTY_ITEM_ERROR,
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
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR,]}
            self._update_errors(e)

    def save(self):
        return ModelForm.save(self)

