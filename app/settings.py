"""
Django settings for project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import posixpath
from HiddenSettings import HiddenSettings
from back.SelectionOptions.LabeledConstants import LOG_FILE
from pathlib import Path

SITE_ID = "1"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = HiddenSettings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = HiddenSettings().GetDebugFlag()

ALLOWED_HOSTS = ['localhost', 'moonmachine.biz', '*']

# Application definition

INSTALLED_APPS = [
    'channels', # some niche cases need this to be defined first for some reason...
    'front',
    'back',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', #blocks django.contrib.staticfiles in development
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', #above all others except security
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware", #required for authentication. place before authenticationmiddleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware' 
]

ROOT_URLCONF = 'urls'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

__static = 'static'
__front = "front"
STATIC_URL = '/static/' #url for the static content must have a forward slash appended and prepended!
STATIC_ROOT = posixpath.join(posixpath.dirname(posixpath.abspath(__file__)), __static)

STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static_pipeline")
    ]


STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATICFILES_FINDERS = ( 
    'django.contrib.staticfiles.finders.FileSystemFinder', 
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
) 

#the django 1.3+ version of TEMPLATE_DIRS
TEMPLATES = [ 
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [            
            os.path.join(BASE_DIR, 'templates')
        ],
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

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + LOG_FILE,
            'formatter': 'dated'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'dated'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True
        },
    },
    'formatters': {
        'dated': {
            'format': "%(created)f; %(levelname)s; %(message)s"
        }
    }
}

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
CSRF_USE_SESSIONS = False #leave as false. if true, it sets the csrf token 

WSGI_APPLICATION = 'wsgi.application'
ASGI_APPLICATION = "asgi.application"


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = HiddenSettings().GetDatabaseConfig()

# fixed bug where django sessions couldnt reset due to sessions middleware

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': '30'
    }
}