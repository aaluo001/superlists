#------------------------------
# functional_tests.test_bills.test_view_bills
#------------------------------
# Author: TangJianwei
# Create: 2019-12-8
#------------------------------
from functional_tests.management.commands.make_bills import make_bills
from functional_tests.server_tools import make_bills_on_server
from commons.utils import date_now, date_now_str

from .base_bills import BillsTest


class ViewBillsTest(BillsTest):

    def test_001(self):
        ''' 新建账单页面，不会显示其他用户的数据
        '''
        # 其他用户新建账单
        self.goto_bill_page('other_user@163.com')
        self.create_bill_normally('100.1', 'other users bills 1')
        self.create_bill_normally('-90.9', 'other users bills 2')
        self.quit_browser()

        # 当前用户访问浏览器
        self.init_browser()
        self.goto_bill_page('abc@163.com')

        # 没有显示账单明细
        self.wait_for(lambda: self.assertEqual(
            self.get_bills(), []
        ))

    def test_002(self):
        ''' 新建账单页面，不会显示当前用户非当天的数据
        '''
        # 创建当前用户的账单明细
        if (self.staging_tests):
            make_bills_on_server('abc@163.com')
        else:
            make_bills('abc@163.com')

        # 当前用户访问浏览器
        self.goto_bill_page('abc@163.com')

        # 没有显示账单明细
        self.wait_for(lambda: self.assertEqual(
            self.get_bills(), []
        ))

    def test_003(self):
        ''' 新建账单页面，可以显示当前用户当天的数据
        '''
        # 新建一条账单
        self.goto_bill_page('abc@163.com')
        self.create_bill_normally('+1000999', 'new bills 1')
        self.create_bill_normally('-2000999', 'new bills 2')
        # 退出浏览器
        self.quit_browser()

        # 再次登录时，新建账单页面会显示当天的数据
        self.init_browser()
        self.goto_bill_page('abc@163.com')
        self.wait_for(lambda: self.assertEqual(
            len(self.get_bills()), 2
        ))

        bill_1_fields = self.get_bill_record_fields(1)
        self.assertEqual(bill_1_fields[0].text, date_now_str())
        self.assertEqual(bill_1_fields[1].text, '-2000999.0')
        self.assertEqual(bill_1_fields[2].text, 'new bills 2')
        
        # 负数显示成红色
        self.assertEqual(
            bill_1_fields[1].find_element_by_css_selector('.text-danger').text,
            bill_1_fields[1].text
        )


        bill_2_fields = self.get_bill_record_fields(2)
        self.assertEqual(bill_2_fields[0].text, date_now_str())
        self.assertEqual(bill_2_fields[1].text, '1000999.0')
        self.assertEqual(bill_2_fields[2].text, 'new bills 1')
        
        # 正数不会显示成红色
        self.assertEqual(
            bill_2_fields[1].find_elements_by_css_selector('.text-danger'),
            []
        )

    def test_004(self):
        ''' 新建账单页面，没有数据不会显示
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 没有显示账单明细
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_id('id_bills_table'), []
        ))


    def test_011(self):
        ''' 账单明细页面，不会显示其他用户的数据
        '''
        # 其他用户新建账单
        self.goto_bill_page('other_user@163.com')
        self.create_bill_normally('100.1', 'other users bills 1')
        self.create_bill_normally('-90.9', 'other users bills 2')
        self.quit_browser()

        # 当前用户访问浏览器
        self.init_browser()
        self.goto_bill_page('abc@163.com')
        self.create_bill_normally('-2000999', 'my bills')

        # 只能看到当前用户的账单明细
        date = date_now()
        self.select_billym(date.year, date.month)
        self.wait_for(lambda: self.assertEqual(
            len(self.get_bills()), 1
        ))
        bill_fields = self.get_bill_record_fields(1)
        self.assertEqual(bill_fields[0].text, date_now_str())
        self.assertEqual(bill_fields[1].text, '-2000999.0')
        self.assertEqual(bill_fields[2].text, 'my bills')

    def test_012(self):
        ''' 账单明细页面，可以显示月账单的所有账单明细
        '''
        # 创建当前用户的账单明细
        if (self.staging_tests):
            make_bills_on_server('abc@163.com')
        else:
            make_bills('abc@163.com')

        # 当前用户访问浏览器
        self.goto_bill_page('abc@163.com')

        # 选择一条月账单，可以看到该月账单所有的账单明细
        self.select_billym(2018, 12)
        self.wait_for(lambda: self.assertEqual(
            len(self.get_bills()), 2
        ))

        bill_1_fields = self.get_bill_record_fields(1)
        self.assertEqual(bill_1_fields[0].text, '2018-12-11')
        self.assertEqual(bill_1_fields[1].text, '32.1')
        self.assertEqual(bill_1_fields[2].text, 'billym_1: old bill 2')

        # 正数不会显示成红色
        self.assertEqual(
            bill_1_fields[1].find_elements_by_css_selector('.text-danger'),
            []
        )

        bill_2_fields = self.get_bill_record_fields(2)
        self.assertEqual(bill_2_fields[0].text, '2018-12-01')
        self.assertEqual(bill_2_fields[1].text, '-9991.1')
        self.assertEqual(bill_2_fields[2].text, 'billym_1: old bill 1')
        
        # 负数显示成红色
        self.assertEqual(
            bill_2_fields[1].find_element_by_css_selector('.text-danger').text,
            bill_2_fields[1].text
        )

    def test_013(self):
        ''' 账单明细页面，不会显示其他未被选择的月账单的账单明细
        '''
        # 创建当前用户的账单明细
        if (self.staging_tests):
            make_bills_on_server('abc@163.com')
        else:
            make_bills('abc@163.com')

        # 当前用户访问浏览器
        self.goto_bill_page('abc@163.com')

        # 可以看到所有的月账单
        billym_elements = self.wait_for(lambda: self.get_billyms())
        self.assertEqual(len(billym_elements), 3)
        self.assertEqual(billym_elements[0].text, '2019年11月')
        self.assertEqual(billym_elements[1].text, '2019年10月')
        self.assertEqual(billym_elements[2].text, '2018年12月')

        # 新建一条账单
        self.create_bill_normally('-2000999', 'my bills')

        # 可以看到刚刚新建的月账单
        date = date_now()
        billym_elements = self.wait_for(lambda: self.get_billyms())
        self.assertEqual(len(billym_elements), 4)
        self.assertEqual(billym_elements[0].text, '{}年{}月'.format(date.year, date.month))
        self.assertEqual(billym_elements[1].text, '2019年11月')
        self.assertEqual(billym_elements[2].text, '2019年10月')
        self.assertEqual(billym_elements[3].text, '2018年12月')

        # 选择刚刚新建的月账单
        self.select_billym(date.year, date.month)
        self.wait_for(lambda: self.assertEqual(
            len(self.get_bills()), 1
        ))
        bill_fields = self.get_bill_record_fields(1)
        self.assertEqual(bill_fields[0].text, date_now_str())
        self.assertEqual(bill_fields[1].text, '-2000999.0')
        self.assertEqual(bill_fields[2].text, 'my bills')

        # 也可以选择其他月账单
        self.select_billym(2019, 11)
        self.wait_for(lambda: self.assertEqual(
            len(self.get_bills()), 2
        ))
        bill_fields = self.get_bill_record_fields(1)
        self.assertEqual(bill_fields[0].text, '2019-11-11')
        self.assertEqual(bill_fields[1].text, '599.1')
        self.assertEqual(bill_fields[2].text, 'billym_3: old bill 2')

        bill_fields = self.get_bill_record_fields(2)
        self.assertEqual(bill_fields[0].text, '2019-11-11')
        self.assertEqual(bill_fields[1].text, '-499.0')
        self.assertEqual(bill_fields[2].text, 'billym_3: old bill 1')

