# coding: utf-8
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'IT',
        'USER': 'postgres',
        'PASSWORD': 'Pbsmtl'
    },
}

POST_TO_BLOCKCHAIN = True

DEBUG = True

ALLOWED_HOSTS = ['domain','127.0.0.1','localhost']

NODE_PRIVATE_KEY = ''
NODE_URL = 'http://127.0.0.1:8000'
