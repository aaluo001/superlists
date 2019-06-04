#!python
# coding: gbk
#------------------------------
# accounts.request_fileter
#------------------------------
# Author: TangJianwei
# Create: 2019-06-01
#------------------------------
import time
import logging


#UNKNOW_USER_AGENT       = '^IP={0}^USER_AGENT={1}^TIME={2}^'
FREQUENTLY_ACCESSED     = '^IP={0}^FREQUENTLY-ACCESSED<{1}s^TIME={2}^'
#SEND_LOGIN_EMAIL        = '^IP={0}^EMAIL={1}^TIME={2}^'

# ����ʱ����
ACCESS_TIME_DELAY       = 5

# ��־
logger = logging.getLogger(__name__)


class RequestFilter(object):
    ''' ���������
    '''
    def __init__(self, request):
        self.request = request

    def get_formatted_time(self):
        return time.strftime('%Y-%m-%d %M:%H:%S')

    def crawl_monitor(self):
        ''' ����������
            [Returns]
                True:  ��⵽�������
                False: ���������
        '''
        session = self.request.session
        access_time = time.time()
        ip_addr = self.request.META.get('REMOTE_ADDR')
        #user_agent = self.request.META.get('HTTP_USER_AGENT')
        
        # Check User-Agent
#        if (user_agent is None \
#            or  'Mozilla' not in user_agent \
#            and 'Safari'  not in user_agent \
#            and 'Chrome'  not in user_agent \
#        ):
#            logger.error(UNKNOW_USER_AGENT.format(ip_addr, user_agent, self.get_formatted_time()))
#            return True

        # Check Access Time
        # ͬһIP�ķ���ʱ����5�����ڣ�����Ϊ�������
        if (session.get('ip_addr') == ip_addr \
            and access_time - session.get('access_time', 0) <= ACCESS_TIME_DELAY
        ):
            logger.error(FREQUENTLY_ACCESSED.format(ip_addr, ACCESS_TIME_DELAY, self.get_formatted_time()))
            return True
        
        # ����Session
        session['ip_addr'] = ip_addr
        session['access_time'] = access_time

        # ��ӡ�����ʼ���Ϣ
#        email = self.request.POST.get('email')
#        if (email):
#            logger.info(SEND_LOGIN_EMAIL.format(ip_addr, email, self.get_formatted_time()))

        # ���������
        return False


