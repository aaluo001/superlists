#------------------------------
# functional_tests.test_bills.test_bill_page
#------------------------------
# Author: TangJianwei
# Create: 2019-11-23
#------------------------------
from commons.utils import date_now, date_now_str
from .base_bills import BillsTest


class CreateBillTest(BillsTest):

    def test_001(self):
        ''' 新建账单
        '''
        # 进入新建账单页面，新建一条账单
        self.goto_bill_page('abc@163.com')
        self.create_bill_normally('1000000.1', 'incomes 1')

        bill_fields = self.get_bill_record_fields(1)
        self.assertEqual(bill_fields[0].text, date_now_str())
        self.assertEqual(bill_fields[1].text, '1000000.1')
        self.assertEqual(bill_fields[2].text, 'incomes 1')
        
        # 正数不会显示成红色
        self.assertEqual(
            bill_fields[1].find_elements_by_css_selector('.text-danger'),
            []
        )

        # 同时，会新建一条月账单
        self.wait_for(lambda: self.assertEqual(
            len(self.get_billyms()), 1
        ))

        # 月账单没有被选中
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_css_selector('#id_billyms_table td.app-selected'),
            []
        ))

        # 月账单会显示某年某月
        date = date_now()
        billym_element = self.get_billym_element(date.year, date.month)
        self.assertRegex(
            billym_element.get_attribute('href'),
            r'/bills/(\d+)/$'
        )


        # 再新建一条账单，并显示出来
        self.create_bill_normally('-9999999.9', 'expends 1')

        bill_fields = self.get_bill_record_fields(1)
        self.assertEqual(bill_fields[0].text, date_now_str())
        self.assertEqual(bill_fields[1].text, '-9999999.9')
        self.assertEqual(bill_fields[2].text, 'expends 1')
        
        # 负数显示成红色
        self.assertEqual(
            bill_fields[1].find_element_by_css_selector('.text-danger').text,
            bill_fields[1].text
        )

        # 还是会显示刚刚的月账单
        self.wait_for(lambda: self.assertEqual(
            len(self.get_billyms()), 1
        ))

        # 月账单没有被选中
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_css_selector('#id_billyms_table td.app-selected'),
            []
        ))

        # 月账单会显示某年某月
        billym_element = self.get_billym_element(date.year, date.month)
        self.assertRegex(
            billym_element.get_attribute('href'),
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
            在收入支出输入框中，执行键盘输入操作时，错误提示会消失
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 输入错误内容后，点击提交
        self.create_bill_failed(money=' ', comment='error money')
        self.assertEqual(
            self.get_error_element_by_id('id_error_money').text,
            '请输入实数！'
        )

        # 在收入支出输入框中，执行键盘输入操作时，错误提示会消失
        money_input_box = self.get_money_input_box()
        money_input_box.send_keys('-10.1')
        self.assertFalse(self.get_error_element_by_id('id_error_money').is_displayed())


    def test_022(self):
        ''' 收入支出：表单检查出错，并显示错误信息2
            在其他输入框中，执行键盘输入操作时，错误提示不会消失
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 输入错误内容后，点击提交
        self.create_bill_failed(money='1.22', comment='error money')
        self.assertEqual(
            self.get_error_element_by_id('id_error_money').text,
            '请不要超过 1 位小数！'
        )

        # 在其他输入框中，执行键盘输入操作时，错误提示不会消失
        comment_input_box = self.get_comment_input_box()
        comment_input_box.send_keys('test')
        self.assertTrue(self.get_error_element_by_id('id_error_money').is_displayed())


    def test_023(self):
        ''' 收入支出：表单检查出错，并显示错误信息3
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 输入错误内容后，点击提交
        self.create_bill_failed(money='12345678', comment='error money')
        self.assertEqual(
            self.get_error_element_by_id('id_error_money').text,
            '请不要超过 7 位整数！'
        )


    def test_031(self):
        ''' 备注：表单检查出错，并显示错误信息1
            在备注输入框中，执行键盘输入操作时，错误提示会消失
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 输入错误内容后，点击提交
        self.create_bill_failed(money='1.0', comment=' ')
        self.assertEqual(
            self.get_error_element_by_id('id_error_comment').text,
            '请输入内容！'
        )

        # 在备注输入框中，执行键盘输入操作时，错误提示会消失
        comment_input_box = self.get_comment_input_box()
        comment_input_box.send_keys('test')
        self.assertFalse(self.get_error_element_by_id('id_error_comment').is_displayed())


    def test_032(self):
        ''' 备注：表单检查出错，并显示错误信息1
            在其他输入框中，执行键盘输入操作时，错误提示不会消失
        '''
        # 进入新建账单页面
        self.goto_bill_page('abc@163.com')

        # 输入错误内容后，点击提交
        self.create_bill_failed(money='1.0', comment=' ')
        self.assertTrue(self.get_error_element_by_id('id_error_comment').is_displayed())

        # 在其他输入框中，执行键盘输入操作时，错误提示不会消失
        money_input_box = self.get_money_input_box()
        money_input_box.send_keys('-10.1')
        self.assertTrue(self.get_error_element_by_id('id_error_comment').is_displayed())

