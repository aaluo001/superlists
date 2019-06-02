#!python
# coding: gbk
#------------------------------
# functional_tests.test_unknow_user_agent
#------------------------------
# Author: TangJianwei
# Create: 2019-06-02
#------------------------------

class UnknowUserAgentTest(object):
    ''' 未知 USER-AGENT 测试
        注意：不能使用 Firefox 浏览器，因此不能继承 FunctionalTest
    '''
    def test_001(self):
        ''' 未知 USER-AGENT
        '''
        self.fail('Finish the test!')

        