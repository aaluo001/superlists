#------------------------------
# bills.templatetags.bill_tags
#------------------------------
# Author: TangJianwei
# Create: 2019-11-23
#------------------------------
from datetime import datetime
from django import template
register = template.Library()

from bills.models import Billym, Bill


@register.inclusion_tag('bills/tag_view_billyms.html')
def view_billyms(owner, selected_billym=None):
    return {
        'billyms': Billym.objects.filter(owner=owner),
        'selected_billym': selected_billym,
    }


@register.inclusion_tag('bills/tag_view_bills.html')
def view_bills(owner, billym_id=None):
    if (billym_id):
        # 选择月账单的账单明细
        return {
            'bills': Bill.objects.select_related('billym')\
                .values('date', 'money', 'comment')\
                .filter(billym__owner=owner)\
                .filter(billym__id=billym_id)
        }

    else:
        # 当天新建账单的账单明细
        return {
            'bills': Bill.objects.select_related('billym')\
                .values('date', 'money', 'comment')\
                .filter(billym__owner=owner)\
                .filter(create_ts__date=datetime.now().date())
        }
