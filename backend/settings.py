
import time

"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from datetime import timedelta

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'VERY_SECRET_KEY_THAT_YOU_SHOULD_CHANGE')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

SESSION_COOKIE_HTTPONLY = False

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'django_filters',
    'webpack_loader',
    'backend',
    'apps.auth_api',
    'pagedown',
    'tagulous',
    'mptt',
    'draceditor',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.vk',
    # 'steem',
]


AUTH_USER_MODEL = 'auth_api.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

APPEND_SLASH = True


SITE_ID = 1

ROOT_URLCONF = 'backend.urls'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_PATH, 'static/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(ROOT_PATH, 'media/')
MEDIA_URL = '/media/'

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))


WSGI_APPLICATION = 'backend.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'backend.authentication.EmailAsUsernameBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
]


WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'apps.auth_api.hasher.MyCryptoHash',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

# JWT authentication
JWT_AUTH = {
    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_EXPIRATION_DELTA': timedelta(seconds=30000),

    'JWT_SECRET_KEY': str(SECRET_KEY),
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,
}


##################
###  TAGULOUS  ###
##################
SERIALIZATION_MODULES = {
    'xml':    'tagulous.serializers.xml_serializer',
    'json':   'tagulous.serializers.json',
    'python': 'tagulous.serializers.python',
    'yaml':   'tagulous.serializers.pyyaml',
}


#################
###  Allauth  ###
#################

ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"


####################
###  Draceditor  ###
####################

# Input: string boolean, `true/false`
DRACEDITOR_ENABLE_CONFIGS = {
    'imgur': 'true',     # to enable/disable imgur uploader/custom uploader.
    'mention': 'true',   # to enable/disable mention
    'jquery': 'true',    # to include/revoke jquery (require for admin default django)
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

# Upload to locale storage
DRACEDITOR_UPLOAD_PATH = 'images/uploads/{}'.format(time.strftime("%Y/%m/%d/"))
DRACEDITOR_UPLOAD_URL = '/api/uploader/'  # change to local uploader


# Maximum Upload Image
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_IMAGE_UPLOAD_SIZE = 5242880  # 5MB
COMPRESS_IMAGE_QUALITY = 50  # Percentage


CORS_ORIGIN_ALLOW_ALL = True


# Post to blockchain or store only internally
POST_TO_BLOCKCHAIN = True
MAIN_TAG = 'itsphere'
POSTING_KEY = '5JgEDJqUKLSK6sD2rCqaPxZ2YAyaxTXmcqmp14WtWJ2BCpFzh4o'
POST_AUTHOR = 'itsphere'
NODE_URL = 'wss://ws.golos.io'

from backend.settings_local import *
