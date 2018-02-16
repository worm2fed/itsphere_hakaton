# coding: utf-8
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mapala',
        'USER': 'postgres',
        'PASSWORD': 'Pbsmtl'
    },
}



DEBUG = True

ALLOWED_HOSTS = ['*']

NODE_PRIVATE_KEY = ''
NODE_URL = 'http://127.0.0.1:8000'
