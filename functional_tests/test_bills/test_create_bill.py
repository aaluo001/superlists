#------------------------------
# functional_tests.test_bills.test_bill_page
#------------------------------
# Author: TangJianwei
# Create: 2019-11-23
#------------------------------
from commons.utils import date_now
from commons.utils import date_now_str
from .base_bills import BillsTest


class CreateBillTest(BillsTest):

    def test_001(self):
        ''' 新建账单
        '''
        # 进入新建账单页面，新建一条账单
        self.goto_bill_page('abc@163.com')
        self.create_bill_normally('1000000.1', 'incomes 1')

        bill_cols = self.browser.find_elements_by_css_selector('#id_bills_row_{} > td'.format(1))
        self.assertEquals(bill_cols[0].text, date_now_str())
        self.assertEquals(bill_cols[1].text, '1000000.1')
        self.assertEquals(bill_cols[2].text, 'incomes 1')
        
        # 正数不会显示成红色
        self.assertEquals(
            bill_cols[1].find_elements_by_css_selector('div.text-danger'),
            []
        )

        # 同时，会新建一条月账单
        self.wait_for(lambda: self.assertEquals(
            len(self.get_billyms()), 1
        ))
        # 月账单没有被选中
        self.assertEquals(
            self.browser.find_elements_by_css_selector('#id_billyms_table tr > td.app-selected'),
            []
        )
        # 月账单会显示某年某月
        date = date_now()
        billym_row = self.browser.find_element_by_css_selector('#id_billyms_row_{}'.format(1))
        self.assertEquals(billym_row.text, '{}年{}月'.format(date.year, date.month))
        self.assertRegex(\
            billym_row.find_element_by_css_selector('a').get_attribute('href'),
            r'/bills/(\d+)/$'
        )


        # 再新建一条账单，并显示出来
        self.create_bill_normally('-9999999.9', 'expends 1')

        bill_cols = self.browser.find_elements_by_css_selector('#id_bills_row_{} > td'.format(1))
        self.assertEquals(bill_cols[0].text, date_now_str())
        self.assertEquals(bill_cols[1].text, '-9999999.9')
        self.assertEquals(bill_cols[2].text, 'expends 1')
        
        # 负数不会显示成红色
        self.assertEquals(
            bill_cols[1].find_element_by_css_selector('div.text-danger').text,
            '-9999999.9'
        )

        # 还是会显示刚刚的月账单
        self.wait_for(lambda: self.assertEquals(
            len(self.get_billyms()), 1
        ))
        # 月账单没有被选中
        self.assertEquals(
            self.browser.find_elements_by_css_selector('#id_billyms_table tr > td.app-selected'),
            []
        )
        # 月账单会显示某年某月
        date = date_now()
        billym_row = self.browser.find_element_by_css_selector('#id_billyms_row_{}'.format(1))
        self.assertEquals(billym_row.text, '{}年{}月'.format(date.year, date.month))
        self.assertRegex(\
            billym_row.find_element_by_css_selector('a').get_attribute('href'),
            r'/bills/(\d+)/$'
        )


    def test_011(self):
        ''' 没有输入内容，直接点击提交
            浏览器会捕获异常
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 没有输入收入支出，点击提交
        self.create_bill(money='', comment='')
        # 浏览器截获了请求，页面不会被加载
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_money:invalid')
        )

        # 没有输入备注，点击提交
        self.create_bill(money='1.1', comment='')
        # 浏览器截获了请求，页面不会被加载
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_comment:invalid')
        )


    def test_021(self):
        ''' 收入支出：表单检查出错，并显示错误信息1
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 输入错误内容后，点击提交
        self.create_bill_failed(money=' ', comment='error money')
        self.wait_for(lambda: self.assertEquals(
            self.get_error_element().text,
            '请输入实数！'
        ))

    def test_022(self):
        ''' 收入支出：表单检查出错，并显示错误信息2
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 输入错误内容后，点击提交
        self.create_bill_failed(money='1.22', comment='error money')
        self.wait_for(lambda: self.assertEquals(
            self.get_error_element().text,
            '请不要超过 1 位小数！'
        ))

    def test_023(self):
        ''' 收入支出：表单检查出错，并显示错误信息3
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 输入错误内容后，点击提交
        self.create_bill_failed(money='12345678', comment='error money')
        self.wait_for(lambda: self.assertEquals(
            self.get_error_element().text,
            '请不要超过 7 位整数！'
        ))


    def test_031(self):
        ''' 备注：表单检查出错，并显示错误信息1
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 输入错误内容后，点击提交
        self.create_bill_failed(money='1.0', comment=' ')
        self.wait_for(lambda: self.assertEquals(
            self.get_error_element().text,
            '请输入内容！'
        ))
