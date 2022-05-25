"""
per-instance settings are in /path/to/app/app.cfg
example settings can be found in /path/to/app/elife.cfg
./install.sh will create a symlink from elife.cfg -> app.cfg if app.cfg not found."""

import os
from os.path import join
import configparser as configparser

PROJECT_NAME = "elife-article-scheduler"

# Build paths inside the project like this: os.path.join(SRC_DIR, ...)
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # "/path/to/app/src/"
PROJECT_DIR = os.path.dirname(SRC_DIR) # "/path/to/app/"

CFG_NAME = 'app.cfg'
DYNCONFIG = configparser.ConfigParser(**{
    'allow_no_value': True,
    'defaults': {'dir': SRC_DIR, 'project': PROJECT_NAME}})
DYNCONFIG.read(join(PROJECT_DIR, CFG_NAME)) # "/path/to/app/app.cfg"

def cfg(path, default=0xDEADBEEF):
    lu = {'True': True, 'true': True, 'False': False, 'false': False} # cast any obvious booleans
    try:
        val = DYNCONFIG.get(*path.split('.'))
        return lu.get(val, val)
    except (configparser.NoOptionError, configparser.NoSectionError): # given key in section hasn't been defined
        if default == 0xDEADBEEF:
            raise ValueError("no value/section set for setting at %r" % path)
        return default
    except Exception as err:
        print('error on %r: %s' % (path, err))

# publishing service hostname not localhost as its https
DASHBOARD_PUBLISHING_SERVICE = cfg('app.dashboard-publishing-service', '')
PUBLISHING_SERVICE_USER = cfg('app.publishing-service-user', '')
PUBLISHING_SERVICE_PASSWORD = cfg('app.publishing-service-password', '')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# this is the 'src' directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = cfg('general.secret-key')

DEBUG = cfg('general.debug')
assert isinstance(DEBUG, bool), "'debug' must be either True or False as a boolean, not %r" % (DEBUG, )

ALLOWED_HOSTS = cfg('general.allowed-hosts', '').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'schedule',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': cfg('general.debug'),
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# https://docs.djangoproject.com/en/3.2/ref/settings/#append-slash
APPEND_SLASH = True

# Database

DATABASES = {
    'default': {
        'ENGINE': cfg('database.engine'),
        'NAME': cfg('database.name'),
        'USER': cfg('database.user'),
        'PASSWORD': cfg('database.password'),
        'HOST': cfg('database.host'),
        'PORT': cfg('database.port'),
    }
}

CONN_MAX_AGE = 0 # 0 = no pooling

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(SRC_DIR, '%s.log' % PROJECT_NAME),
            'formatter': 'verbose'
        },
        'debug-console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'schedule': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
