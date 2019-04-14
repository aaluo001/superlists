#!python
# coding: gbk
#------------------------------
# server_tools.py
#------------------------------
# author: TangJianwei
# update: 2019-04-14
#------------------------------
from fabric.api import run
from fabric.context_managers import settings


# 过渡服务器
STAGING_USER   = 'root'
STAGING_HOST   = '47.97.118.237'
STAGING_SERVER = 'www.tjw-superlists-staging.site'


def _manage():
    return '~/sites/{0}/virtualenv/bin/python ~/sites/{0}/source/manage.py'.format(STAGING_SERVER)

def _host_string():
    return STAGING_USER + '@' + STAGING_HOST


def reset_database():
    with settings(host_string=_host_string()):
        run(_manage() + ' flush --noinput')


def create_session_on_server(email):
    with settings(host_string=_host_string()):
        session_key = run(_manage() + ' create_session ' + email)
        return session_key.strip()

