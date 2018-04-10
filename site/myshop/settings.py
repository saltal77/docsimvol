# coding: utf-8
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
GOOGLE_RECAPTCHA_SECRET_KEY = '6Ldo-XXXXXXXXXXXXXXXXXXXXXXXXXIq9yIN0892'

DEBUG = False


ALLOWED_HOSTS = ['www.docsimvol.ru', 'docsimvol.ru']

CART_SESSION_ID = 'docsimvol'

SUIT_CONFIG = {
    'ADMIN_NAME': 'Adminka DocSimvol',
    'MENU_ICONS': {
        'shop': 'icon-folder-open',
        'auth': 'icon-lock',
        'cupons': 'icon-qrcode',
        'orders': 'icon-shopping-cart',
    }
}

THUMBNAIL_BASEDIR = 'thumbnails'
THUMBNAIL_DEFAULT_OPTIONS = { 'crop': 'smart', 'detail': True}
#THUMBNAIL_DEBUG = True

CACHES = {
  'default': {
      'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
      'LOCATION': '/var/tmp/docsimvol_cache',
      'TIMEOUT': 300,
  }
}


INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'cart',
    'orders',
    'cupons',
    'easy_thumbnails',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myshop',
        'USER': 'XXXXXXXXXX',
        'PASSWORD': 'XXXXXXXXXXX',
        'HOST': 'localhost',
        'PORT': '',
    }
}


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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_HOST = 'smtp.mailserver.ru'
EMAIL_HOST_PASSWORD = 'XXXXXXXXXXXX'
EMAIL_HOST_USER = 'XXXXXX@docsimvol.ru'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
SERVER_EMAIL = 'XXXXXXX@docsimvol.ru'
DEFAULT_FROM_EMAIL = 'XXXXXXXX@docsimvol.ru'
EMAIL_SUBJECT_PREFIX = "docsimvol.ru: "
STUFF_EMAIL = 'XXXXXXX@docsimvol.ru'
ORDER_EMAIL = 'XXXXXXX@docsimvol.ru'
