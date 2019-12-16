#------------------------------
# functional_tests.test_bills.test_select_billym
#------------------------------
# Author: TangJianwei
# Create: 2019-12-16
#------------------------------
from functional_tests.management.commands.make_bills import make_bills
from functional_tests.server_tools import make_bills_on_server

from commons.utils import date_now
from .base_bills import BillsTest


class SelectBillymTest(BillsTest):

    def test_001(self):
        ''' 不会统计其他用户的账单
            确认只有支出时的统计结果
        '''
        # 其他用户新建账单
        self.goto_bill_page('other_user@163.com')
        self.create_bill_normally('1000990.1', 'other users bills')
        self.quit_browser()

        # 当前用户访问浏览器
        self.init_browser()
        self.goto_bill_page('abc@163.com')
        self.create_bill_normally('-2000999.1', 'my bills')

        # 只能看到当前用户的统计账单
        date = date_now()
        self.select_billym(date.year, date.month)
        aggs = self.wait_for(lambda: 
            self.browser.find_elements_by_css_selector('#id_aggs_row td')
        )

        self.assertEqual(aggs[0].text, '0')
        self.assertEqual(aggs[1].text, '-2000999.1')
        self.assertEqual(aggs[2].text, '-2000999.1')

        self.assertNotIn('text-danger', aggs[0].get_attribute('class'))
        self.assertIn('text-danger', aggs[1].get_attribute('class'))
        self.assertIn('text-danger', aggs[2].get_attribute('class'))

    def test_002(self):
        ''' 只是统计被选中的月账单
            确认只有收入时的统计结果
        '''
        # 创建当前用户的账单明细
        if (self.staging_tests):
            make_bills_on_server('abc@163.com')
        else:
            make_bills('abc@163.com')

        # 当前用户访问浏览器
        self.goto_bill_page('abc@163.com')

        # 只是统计被选中的月账单
        self.select_billym(2019, 10)
        aggs = self.wait_for(lambda: 
            self.browser.find_elements_by_css_selector('#id_aggs_row td')
        )

        self.assertEqual(aggs[0].text, '912.9')
        self.assertEqual(aggs[1].text, '0')
        self.assertEqual(aggs[2].text, '912.9')

        self.assertNotIn('text-danger', aggs[0].get_attribute('class'))
        self.assertNotIn('text-danger', aggs[1].get_attribute('class'))
        self.assertNotIn('text-danger', aggs[2].get_attribute('class'))

    def test_003(self):
        ''' 统计多条账单明细
        '''
        # 当前用户访问浏览器
        self.goto_bill_page('abc@163.com')
        date = date_now()

        # 余额正好为零
        self.create_bill_normally('+1', 'my bills 1')
        self.create_bill_normally('-1', 'my bills 2')

        self.select_billym(date.year, date.month)
        aggs = self.wait_for(lambda: 
            self.browser.find_elements_by_css_selector('#id_aggs_row td')
        )

        self.assertEqual(aggs[0].text, '1.0')
        self.assertEqual(aggs[1].text, '-1.0')
        self.assertEqual(aggs[2].text, '0.0')

        self.assertNotIn('text-danger', aggs[0].get_attribute('class'))
        self.assertIn('text-danger', aggs[1].get_attribute('class'))
        self.assertNotIn('text-danger', aggs[2].get_attribute('class'))

        # 返回新建账单页面
        self.browser.find_element_by_link_text('新建账单').click()

        # 新建账单
        self.create_bill_normally('+8900.3', 'my bills 3')
        self.create_bill_normally('-5600.7', 'my bills 4')
        self.create_bill_normally('-10.0', 'my bills 5')
        self.create_bill_normally('-625.2', 'my bills 6')
        self.create_bill_normally('+300', 'my bills 7')

        self.select_billym(date.year, date.month)
        aggs = self.wait_for(lambda: 
            self.browser.find_elements_by_css_selector('#id_aggs_row td')
        )

        incomes = round(1 + 8900.3 + 300, 1)
        expends = round(-1 - 5600.7 - 10.0 - 625.2, 1)
        balance = round(incomes + expends, 1)
        self.assertEqual(aggs[0].text, str(incomes))
        self.assertEqual(aggs[1].text, str(expends))
        self.assertEqual(aggs[2].text, str(balance))
