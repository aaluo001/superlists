#====================
# 过渡服务器测试说明
#====================

## 过渡服务器测试开始之前，需要设置环境变量

* 过渡服务器访问密码
  export STAGING_SERVER_PASSWORD=******

* 测试邮箱密码
  export TEST_EMAIL_PASSWORD=******


## 过渡服务器测试命令

STAGING_TESTS=yes python manage.py test functional_tests.test_accounts
STAGING_TESTS=yes python manage.py test functional_tests.test_lists

