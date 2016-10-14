"""
Django settings for direitoemtela project.

Generated by 'django-admin startproject' using Django 1.8.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import keys
from easy_thumbnails.conf import Settings as thumbnail_settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'l6a_1lygw=vra_4bep1c^*ws14!n=2seg-jb!6f%8&clrtnm_q'
SECRET_KEY = keys.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['local.det.com', 'direitoemtela.com.br',]

EMAIL_HOST = 'smtp.sendgrid.net'

EMAIL_HOST_USER = 'direitoemtela'

EMAIL_HOST_PASSWORD = keys.EMAIL_HOST_PASSWORD

EMAIL_PORT = 587

EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easy_timezones',
    'storages',
    'compressor',
    'main',
    'search',
    'videos',
    'categories',
    'mailing',
    'easy_thumbnails',
    'image_cropping',
    'autoupdate',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'easy_timezones.middleware.EasyTimezoneMiddleware',
)

APPEND_SLASH = True

ROOT_URLCONF = 'direitoemtela.urls'

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
SITE_ROOT = PROJECT_ROOT


MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
    os.path.join(SITE_ROOT, 'main/templates'),
    os.path.join(SITE_ROOT, 'search/templates'),
)

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # cant contain static_root
    os.path.join(SITE_ROOT, 'devstatic/'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

WSGI_APPLICATION = 'direitoemtela.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': keys.DATABASE_HOST,
        'PORT': keys.DATABASE_PORT,
        'NAME': keys.DATABASE_NAME,
        'USER': keys.DATABASE_USER,
        'PASSWORD': keys.DATABASE_PASSWORD,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_TZ = True

USE_I18N = True

USE_L10N = True

USE_TZ = True

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YT_CHANNEL_ID = 'UCOEfipXIvMmAHgg8XPcBtag'
YT_KEY = keys.YT_KEY

GEOIP_DATABASE = os.path.join(SITE_ROOT, 'geoip/GeoLiteCity.dat')
GEOIPV6_DATABASE = os.path.join(SITE_ROOT, 'geoip/GeoLiteCityv6.dat')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/




try:
    from .dev_settings import *
except:
    from .production_settings import *
