#------------------------------
# bills.forms
#------------------------------
# Author: TangJianwei
# Create: 2019-10-21
#------------------------------
from datetime import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from commons.messages import ERROR_MESSAGES
from bills.models import Billym, Bill


class BillForm(ModelForm):
    '''
    '''
    # ---------- 项目定义 ----------
    class Meta:
        model = Bill
        fields = ('money', 'comment', )
        widgets = {
            # 金额
            'money': forms.TextInput(
                attrs={
                    'placeholder': '负数为支出，正数为收入',
                    'class': 'form-control',
                }
            ),
            # 备注
            'comment': forms.TextInput(
                attrs={
                    'placeholder': '金额的使用说明',
                    'class': 'form-control',
                }
            ),
        }
        error_messages = {
            # 金额
            'money': {
                'required': ERROR_MESSAGES['required'].format('金额'),
                'invalid': ERROR_MESSAGES['invalid_decimal'].format('金额'),
                'max_digits': ERROR_MESSAGES['max_digits'].format('金额', '8'),
                'max_whole_digits': ERROR_MESSAGES['max_whole_digits'].format('金额', '7'),
                'max_decimal_places': ERROR_MESSAGES['max_decimal_places'].format('金额', '1'),
            },
            # 备注
            'comment': {
                'required': ERROR_MESSAGES['required'].format('备注'),
                'max_length': ERROR_MESSAGES['max_length'].format('备注', '32'),
            },
        }
 

    # ---------- 保存到数据库 ----------
    def save(self, owner):
        date = datetime.now().date()
        self.instance.billym, _ = Billym.objects.get_or_create(\
            owner=owner, year=date.year, month=date.month
        )
        # 账单发生日期为当天
        self.instance.date = date
        return super().save()

