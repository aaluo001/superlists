#------------------------------
# lists.forms
#------------------------------
# Author: TangJianwei
# Create: 2019-03-10
#------------------------------
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from commons.messages import ERROR_MESSAGES
from lists.models import Item


class ItemForm(ModelForm):
    
    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.fields.TextInput(
                attrs={
                    'placeholder': '输入待办事项',
                    'class': 'form-control',
                    'maxlength': '32',
                }
            )
        }
        error_messages = {
            'text': {
                'required': ERROR_MESSAGES['required'].format('待办事项'),
            }
        }


    def clean_text(self):
        ''' 编辑待办事项的内容
        '''
        data = self.cleaned_data['text']
        if (len(data) > 32):
            raise ValidationError(\
                ERROR_MESSAGES['max_length'].format('待办事项', '32'))
        return data

    
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
            e.error_dict = {'text': ['您已经提交一个同样的待办事项！',]}
            self._update_errors(e)

    def save(self):
        return ModelForm.save(self)

