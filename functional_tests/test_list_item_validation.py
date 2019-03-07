#!python
# coding: gbk
#------------------------------
# test_list_item_validation.py
#------------------------------
# author: TangJianwei
# update: 2019-02-25
#------------------------------
from selenium.webdriver.common.keys import Keys
#from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.fail('write me!')

