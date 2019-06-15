#------------------------------
# functional_tests.test_frequently_accessed
#------------------------------
# Author: TangJianwei
# Create: 2019-06-01
#------------------------------
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class FrequentlyAccessedTest(FunctionalTest):
    ''' 频繁访问测试
    '''
    def test_001(self):
        ''' 连续时间间隔内多次发送登录验证邮件
        '''
        if (self.staging_tests):
            test_email = 'superlists_tests@163.com'
        else:
            test_email = 'abc@163.com'

        # 第一次发送登录验证邮件
        self.browser.get(self.live_server_url)
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # 检测到“邮件发送成功”的消息
        self.wait_for(lambda: self.assertIn(
            '邮件发送成功',
            self.browser.find_element_by_id('id_messages').text
        ))
 

        # 第二次发送登录验证邮件
        input_email = self.browser.find_element_by_name('email')
        input_email.send_keys(test_email)
        input_email.send_keys(Keys.ENTER)
        
        # 由于时间间隔不够(5秒)，提示“系统繁忙”的消息
        self.wait_for(lambda: self.assertIn(
            '系统繁忙',
            self.browser.find_element_by_id('id_messages').text
        ))

