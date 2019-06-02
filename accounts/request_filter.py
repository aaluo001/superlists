#!python
# coding: gbk
#------------------------------
# accounts.request_fileter
#------------------------------
# Author: TangJianwei
# Create: 2019-06-01
#------------------------------
import time
from sys import stdout, stderr


UNKNOW_USER_AGENT       = '^IP={0}^USER_AGENT={1}^TIME={2}^\n'
FREQUENTLY_ACCESSED     = '^IP={0}^FREQUENTLY-ACCESSED<{1}s^TIME={2}^\n'
SEND_LOGIN_EMAIL        = '^IP={0}^EMAIL={1}^TIME={2}^\n'

# 访问时间间隔
ACCESS_TIME_DELAY       = 5


class RequestFilter(object):
    ''' 请求过滤器
    '''
    def __init__(self, request):
        self.request = request

    def get_formatted_time(self):
        return time.strftime('%Y-%m-%d %M:%H:%S')

    def crawl_monitor(self):
        ''' 反爬虫监测器
            [Returns]
                True:  监测到爬虫程序
                False: 非爬虫程序
        '''
        # Check User-Agent
        ip_addr = self.request.META.get('REMOTE_ADDR')
        user_agent = self.request.META.get('HTTP_USER_AGENT')
        if (user_agent is None \
            or  'Mozilla' not in user_agent \
            and 'Safari'  not in user_agent \
            and 'Chrome'  not in user_agent \
        ):
            stdout.write(UNKNOW_USER_AGENT.format(ip_addr, user_agent, self.get_formatted_time()))
            return True

        # Check Access Time
        # 同一IP的访问时间在5秒以内，则视为爬虫程序
        session = self.request.session
        access_time = time.time()
        if (session.get('ip_addr') == ip_addr \
            and access_time - session.get('access_time', 0) <= ACCESS_TIME_DELAY
        ):
            stderr.write(FREQUENTLY_ACCESSED.format(ip_addr, ACCESS_TIME_DELAY, self.get_formatted_time()))
            return True
        
        # 设置Session
        session['ip_addr'] = ip_addr
        session['access_time'] = access_time

        # 打印发送邮件信息
        email = self.request.POST.get('email')
        if (email):
            stdout.write(SEND_LOGIN_EMAIL.format(ip_addr, email, self.get_formatted_time()))

        # 非爬虫程序
        return False


