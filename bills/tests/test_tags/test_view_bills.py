#------------------------------
# bills.tests.test_tags.test_view_billyms
#------------------------------
# Author: TangJianwei
# Create: 2019-11-24
#------------------------------
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from bills.models import Billym, Bill
from bills.templatetags.bill_tags import view_bills


class ViewBillsTest(TestCase):

    def test_001(self):
        '''
        '''
        self.fail('Finished the test!')



