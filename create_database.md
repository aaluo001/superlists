#====================
# 创建测试数据库
#====================

# 创建测试用户dev001
  CREATE ROLE dev001 LOGIN PASSWORD 'dev001#' CREATEDB;
  
# 创建和用户名同名的数据库
  CREATE DATABASE dev001 WITH OWNER = dev001;


# 修改settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dev001',
        'USER': 'dev001',
        'PASSWORD': 'dev001#',
    }
}

# 创建测试用table
  python manage.py migrate

