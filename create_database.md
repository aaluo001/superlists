#====================
# 创建测试数据库
#====================

# 创建测试用户dev001
  create user dev001 with createdb password 'dev001#';
  
# 创建和用户名同名的数据库
  create database dev001;

# 改变数据所属到用户dev001
  alter database dev001 owner to dev001;


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

