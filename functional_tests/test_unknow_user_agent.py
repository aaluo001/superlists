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
    ''' δ֪ USER-AGENT ����
        ע�⣺����ʹ�� Firefox ���������˲��ܼ̳� FunctionalTest
              ���ǣ�Ҳ����ʹ�� PhantomJS �����
    '''
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    
    def test_001(self):
        ''' δ֪ USER-AGENT
        '''
        self.fail('Finish the test!')

        