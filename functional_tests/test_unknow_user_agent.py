#!python
# coding: gbk
#------------------------------
# functional_tests.test_unknow_user_agent
#------------------------------
# Author: TangJianwei
# Create: 2019-06-02
#------------------------------
from django.contrib.staticfiles.testing import StaticLiveServerTestCase



class UnknowUserAgentTest(StaticLiveServerTestCase):
    ''' 未知 USER-AGENT 测试
        注意：不能使用 Firefox 浏览器，因此不能继承 FunctionalTest
              但是，也不能使用 PhantomJS 浏览器
    '''
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    
    def test_001(self):
        ''' 未知 USER-AGENT
        '''
        self.fail('Finish the test!')

        