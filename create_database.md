#====================
# �����������ݿ�
#====================

# ���������û�dev001
  CREATE ROLE dev001 LOGIN PASSWORD 'dev001#' CREATEDB;
  
# �������û���ͬ�������ݿ�
  CREATE DATABASE dev001 WITH OWNER = dev001;


# �޸�settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dev001',
        'USER': 'dev001',
        'PASSWORD': 'dev001#',
    }
}

# ����������table
  python manage.py migrate

