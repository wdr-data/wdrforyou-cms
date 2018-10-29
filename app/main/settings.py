"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

DEBUG = False
if os.environ.get("DEBUG") == "True":
    DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')
if SECRET_KEY is None:
    if DEBUG:
        SECRET_KEY = '34a!^u+4qx^8_6fa1!7$88u*i_sug@rar1d@og4=glo!&p4k5j'
    else:
        raise EnvironmentError("Please specify a SECRET_KEY in your environment")

ALLOWED_HOSTS = ['*']

if not DEBUG:
    SECURE_SSL_REDIRECT = True

AWS_LAMBDA = os.environ.get('SERVERTYPE') == 'AWS Lambda'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_s3_storage',  # Static files
    'cms.apps.CmsConfig',
    'rest_framework',
    'django_filters',
    'tz_detect',
    'rest_framework.authtoken',
    'emoji_picker',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tz_detect.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'main.urls'

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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if AWS_LAMBDA:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASSWORD'],
            'HOST': os.environ['DB_HOST'],
            'PORT': '5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/admin/login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

if AWS_LAMBDA:
    S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

    DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
    STATICFILES_STORAGE = 'django_s3_storage.storage.ManifestStaticS3Storage'

    AWS_S3_BUCKET_NAME = S3_BUCKET_NAME
    AWS_S3_BUCKET_NAME_STATIC = S3_BUCKET_NAME

    # The AWS region to connect to.
    AWS_REGION = "eu-central-1"

    # The AWS access key to use.
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

    # The AWS secret access key to use.
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    AWS_S3_BUCKET_AUTH = False

else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL[1:])

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL[1:])

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'api.apps.StandardPagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend', ),
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication', ),
}

TZ_DETECT_COUNTRIES = ('DE', 'FR', 'GB', 'US', 'CN', 'IN', 'JP', 'BR', 'RU')
