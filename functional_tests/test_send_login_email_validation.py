#------------------------------
# functional_tests.test_send_login_email_validation
#------------------------------
# Author: TangJianwei
# Create: 2019-05-18
#------------------------------
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class SendLoginEmailValidationTest(FunctionalTest):
    ''' 发送登录邮件验证测试
    '''
    def test_001(self):
        ''' 未输入邮箱地址就发送邮件
        '''
        # 访问首页
        # 未输入邮箱地址就发送邮件
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(Keys.ENTER)

        # 浏览器截获了请求，页面不会被加载
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:invalid')
        )


    def test_002(self):
        ''' 发送错误邮箱地址，会得到发送邮件失败的提示
            而不会出现Server Error (500)
        '''
        # 只能在过渡网站中测试
        if (not self.staging_tests): return
        
        # 访问首页
        # 在导航栏的登录区域输入错误的邮箱地址
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys('error_email_tests@163.com')
        input_email.send_keys(Keys.ENTER)
        
        # 检测到“邮件发送失败”的消息
        self.wait_for(lambda: self.assertIn(
            '邮件发送失败',
            self.browser.find_element_by_id('id_messages').text
        ))

        # 没有检测到“ServerError(500)”
        self.assertNotIn('Server Error (500)', self.browser.page_source)

