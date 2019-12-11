#------------------------------
# functional_tests.test_bills.base_bills
#------------------------------
# Author: TangJianwei
# Create: 2019-11-23
#------------------------------
from selenium.webdriver.common.keys import Keys

from functional_tests.base import wait
from functional_tests.base import FunctionalTest

from commons.utils import date_now


class BillsTest(FunctionalTest):

    def goto_bill_page(self, login_email):
        self.create_pre_authenticated_session(login_email)
        self.browser.get(self.live_server_url)
        navbar = self.browser.find_element_by_id('id_navigation')
        navbar.find_element_by_link_text('应用').click()
        navbar.find_element_by_link_text('账单').click()


    def get_money_input_box(self):
        return self.browser.find_element_by_id('id_money')

    def get_comment_input_box(self):
        return self.browser.find_element_by_id('id_comment')

    def get_submit_button(self):
        return self.browser.find_element_by_css_selector('form.form-horizontal button.btn.btn-primary')

    def get_bills(self):
        return self.browser.find_elements_by_css_selector('#id_bills_table > tbody > tr')

    def get_billyms(self):
        return self.browser.find_elements_by_css_selector('#id_billyms_table tr')


    def create_bill(self, money, comment):
        self.get_money_input_box().send_keys(money)
        self.get_comment_input_box().send_keys(comment)
        self.get_submit_button().send_keys(Keys.ENTER)

    def create_bill_normally(self, money, comment):
        row_num = self.wait_for(lambda: len(self.get_bills()))
        self.create_bill(money, comment)
        self.wait_for(lambda: self.assertEquals(
            len(self.get_bills()), row_num + 1
        ))

    def create_bill_failed(self, money, comment):
        row_num = self.wait_for(lambda: len(self.get_bills()))
        self.create_bill(money, comment)
        self.get_error_element()
        self.wait_for(lambda: self.assertEquals(
            len(self.get_bills()), row_num
        ))


    def get_bill_record_fields(self, row_num):
        return self.wait_for(lambda: 
            self.browser.find_elements_by_css_selector('#id_bills_row_{} > td'.format(row_num))
        )

    def get_billym_element(self, date=date_now(), row_num=None):
        billyms_panel = self.wait_for(lambda:
            self.browser.find_element_by_id('id_view_billyms')
        )
        if (row_num):
            return self.wait_for(lambda:
                billyms_panel.find_element_by_id('id_billyms_row_{}'.format(row_num))
            )
        else:
            return self.wait_for(lambda:
                billyms_panel.find_element_by_link_text('{}年{}月'.format(date.year, date.month))
            )

    def select_billym(self, date=date_now()):
        self.get_billym_element(date).click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('#id_jumbotron > h1').text,
            '账单明细'
        ))

