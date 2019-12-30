#------------------------------
# lists.templatetags.list_tags
#------------------------------
# Author: TangJianwei
# Create: 2019-11-23
#------------------------------
from django import template
register = template.Library()

from lists.models import List


@register.inclusion_tag('lists/tag_view_mylists.html')
def view_mylists(owner, selected_list=None):
    return {
        'list_set': List.objects.filter(owner=owner),
        'selected_list': selected_list,
    }
