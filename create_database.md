#====================
# �����������ݿ�
#====================

# ���������û�dev001
  create user dev001 with createdb password 'dev001#';
  
# �������û���ͬ�������ݿ�
  create database dev001;

# �ı������������û�dev001
  alter database dev001 owner to dev001;


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

