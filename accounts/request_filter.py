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


# ��־
LOG = logging.getLogger(__name__)


class RequestFilter(object):
    ''' ���������
    '''
    def __init__(self, request):
        self.request = request

    def crawl_monitor(self, delay=3):
        ''' ����������
            [Params]
                delay: �ӳټ�飨�뵥λ��
            [Returns]
                True:  ��⵽�������
                False: ���������
        '''
        session = self.request.session
        access_time = time.time()
        
        ip_addr = None
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if (x_forwarded_for):
            ip_addr = x_forwarded_for.split(',')[0]
        else:
            ip_addr = self.request.META.get('REMOTE_ADDR')
        
        #user_agent = self.request.META.get('HTTP_USER_AGENT')
        
        # Check User-Agent
#        if (user_agent is None \
#            or  'Mozilla' not in user_agent \
#            and 'Safari'  not in user_agent \
#            and 'Chrome'  not in user_agent \
#        ):
#            return True

        # Check Access Time
        # ͬһIP�ķ���ʱ����5�����ڣ�����Ϊ�������
        if (session.get('ip_addr') == ip_addr \
            and access_time - session.get('access_time', 0) <= delay
        ):
            LOG.error('frequently accessed error: ' + ip_addr)
            return True
        
        # ���������
        session['ip_addr'] = ip_addr
        session['access_time'] = access_time
        return False

