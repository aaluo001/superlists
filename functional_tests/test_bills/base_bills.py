#------------------------------
# functional_tests.test_bills.base_bills
#------------------------------
# Author: TangJianwei
# Create: 2019-11-23
#------------------------------
from selenium.webdriver.common.keys import Keys

from functional_tests.base import wait
from functional_tests.base import FunctionalTest


class BillsTest(FunctionalTest):

    def get_input_box(self, id):
        return self.browser.find_element_by_id(id)

