#------------------------------
# server_tools.py
#------------------------------
# author: TangJianwei
# update: 2019-04-14
#------------------------------
import os
from fabric.api import env, run
from fabric.context_managers import settings


# 过渡服务器
STAGING_USER_ROOT = 'root'
# STAGING_DATABASE  = 'dev001'
STAGING_HOST      = '47.97.118.237'
STAGING_SERVER    = 'www.tjw-superlists-staging.site'


def _manage():
    return '~/sites/{0}/virtualenv/bin/python ~/sites/{0}/source/manage.py'.format(STAGING_SERVER)

def _host_root():
    env.password = os.environ['STAGING_ROOT_PW']
    return STAGING_USER_ROOT + '@' + STAGING_HOST


def reset_database():
    with settings(host_string=_host_root()):
        run(_manage() + ' flush --noinput')

def create_session_on_server(email):
    with settings(host_string=_host_root()):
        session_key = run(_manage() + ' create_session ' + email)
        return session_key.strip()

def make_bills_on_server(email):
    with settings(host_string=_host_root()):
        run(_manage() + ' make_bills ' + email)


# def execute_sql(sql):
#     with settings(host_string=_host_root()):
#         run('psql -d {} -c "{}"'.format(STAGING_DATABASE, sql))
