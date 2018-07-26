"""
Django settings for bfrs_project project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import dj_database_url
import ldap
import os
import sys

from confy import env, database, cache

from django.contrib.messages import constants as message_constants
MESSAGE_LEVEL = message_constants.DEBUG

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap3'
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 * 4 # 5.0MB * 4

P1CAD_ENDPOINT = env('P1CAD_ENDPOINT') or None
P1CAD_USER = env('P1CAD_USER') or None
P1CAD_PASSWORD = env('P1CAD_PASSWORD') or None
P1CAD_SSL_VERIFY = True if env('P1CAD_SSL_VERIFY',True) else False
P1CAD_NOTIFY_EMAIL = env('P1CAD_NOTIFY_EMAIL') or None

EMAIL_HOST = env('EMAIL_HOST', 'email.host')
EMAIL_PORT = env('EMAIL_PORT', 25)
FROM_EMAIL = env('FROM_EMAIL', 'from_email')
PICA_EMAIL = env('PICA_EMAIL') or None
PVS_EMAIL = env('PVS_EMAIL') or None
FPC_EMAIL = env('FPC_EMAIL') or None
POLICE_EMAIL = env('POLICE_EMAIL') or None
DFES_EMAIL = env('DFES_EMAIL') or None
FSSDRS_EMAIL = env('FSSDRS_EMAIL') or None
EMAIL_TO_SMS_FROMADDRESS = env('EMAIL_TO_SMS_FROMADDRESS') or None
SMS_POSTFIX = env('SMS_POSTFIX', 'sms_postfix')
MEDIA_ALERT_SMS_TOADDRESS_MAP = env('MEDIA_ALERT_SMS_TOADDRESS_MAP') or None
ALLOW_EMAIL_NOTIFICATION = (os.environ.get('ALLOW_EMAIL_NOTIFICATION') or 'false').lower() in ["true", "on", "1", "debug","yes"]
EMAIL_EXCLUSIONS = env('EMAIL_EXCLUSIONS', [])
CC_EMAIL = env('CC_EMAIL') or None
BCC_EMAIL = env('BCC_EMAIL') or None
SUPPORT_EMAIL = env('SUPPORT_EMAIL') or None
MERGE_BUSHFIRE_EMAIL = env('MERGE_BUSHFIRE_EMAIL') or None

INTERNAL_EMAIL = env('INTERNAL_EMAIL',['dbca.wa.gov.au','dpaw.wa.gov.au'])
SSS_URL = env('SSS_URL', 'sss_redirect_url')
AREA_THRESHOLD = env('AREA_THRESHOLD', 2)

PBS_URL = env('PBS_URL', 'https://pbs.dpaw.wa.gov.au/')
URL_SSO = env('URL_SSO', 'https://oim.dpaw.wa.gov.au/api/users/')
USER_SSO = env('USER_SSO')
PASS_SSO = env('PASS_SSO')
FSSDRS_USERS = env('FSSDRS_USERS')
FSSDRS_GROUP = env('FSSDRS_GROUP', 'FSS Datasets and Reporting Services')

HARVEST_EMAIL_HOST = env('HARVEST_EMAIL_HOST')
HARVEST_EMAIL_USER = env('HARVEST_EMAIL_USER')
HARVEST_EMAIL_PASSWORD = env('HARVEST_EMAIL_PASSWORD')
HARVEST_EMAIL_FOLDER = env('HARVEST_EMAIL_FOLDER', 'INBOX')

# Outstanding Fires Report
GOLDFIELDS_EMAIL = env('GOLDFIELDS_EMAIL') or None
KIMBERLEY_EMAIL = env('KIMBERLEY_EMAIL') or None
MIDWEST_EMAIL = env('MIDWEST_EMAIL') or None
PILBARA_EMAIL = env('PILBARA_EMAIL') or None
SOUTH_COAST_EMAIL = env('SOUTH_COAST_EMAIL') or None
SOUTH_WEST_EMAIL = env('SOUTH_WEST_EMAIL') or None
SWAN_EMAIL = env('SWAN_EMAIL') or None
WARREN_EMAIL = env('WARREN_EMAIL') or None
WHEATBELT_EMAIL = env('WHEATBELT_EMAIL') or None
OUTSTANDING_FIRES_EMAIL=[ 
    {"Goldfields": GOLDFIELDS_EMAIL}, 
    {"Kimberley": KIMBERLEY_EMAIL},
    {"Midwest": MIDWEST_EMAIL},
    {"Pilbara": PILBARA_EMAIL},
    {"South Coast": SOUTH_COAST_EMAIL},
    {"South West": SOUTH_WEST_EMAIL},
    {"Swan": SWAN_EMAIL},
    {"Warren": WARREN_EMAIL},
    {"Wheatbelt": WHEATBELT_EMAIL},
]
#if ALL_REGIONS_EMAIL: OUTSTANDING_FIRES_EMAIL.append({"All Regions": ALL_REGIONS_EMAIL})
     
HISTORICAL_CAUSE_CSV_FILE = env('HISTORICAL_CAUSE_CSV_FILE', '')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
#SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = (os.environ.get('DEBUG') or 'false').lower() in ["true", "on", "1", "yes", "debug"]

ALLOWED_HOSTS = []

#DEBUG = os.environ.get('DEBUG', None) in ["True", "on", "1", "DEBUG"]
INTERNAL_IPS = ['127.0.0.1', '::1']

ALLOWED_HOSTS = env("ALLOWED_HOSTS",['bfrs.dpaw.wa.gov.au','bfrs.dbca.wa.gov.au'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    #'guardian',
    'reversion',
    'reversion_compare',
    'tastypie',
    'smart_selects',
    'django_extensions',
    'debug_toolbar',
    'crispy_forms',
    'django_filters',

    'bfrs',
]

ADD_REVERSION_ADMIN=True

MIDDLEWARE_CLASSES = [
#    'django.middleware.security.SecurityMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
#    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
#    'dpaw_utils.middleware.SSOLoginMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'dpaw_utils.middleware.SSOLoginMiddleware',

]

ROOT_URLCONF = 'bfrs_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'bfrs', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
#            'loaders': [
#                'django.template.loaders.cached.Loader',
#                'django.template.loaders.filesystem.Loader',
#                'django.template.loaders.app_directories.Loader',
#            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'bfrs_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {'default': database.config()}
#DATABASES = {'default': dj_database_url.config()}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #'guardian.backends.ObjectPermissionBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Australia/Perth'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
         'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'compressor.finders.CompressorFinder',

)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            #'stream': sys.stdout,
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            #'class': 'logging.FileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/bfrs.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'bfrs': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    }

}

if DEBUG:
    LOGGING['loggers']['django.request']['level'] = 'DEBUG'
    LOGGING['loggers']['bfrs']['level'] = 'DEBUG'


ENV_TYPE = env('ENV_TYPE') or None
if not ENV_TYPE:
    try:
        ENV_TYPE = os.getcwd().split('-')[1].split('.')[0] # will return either 'dev' or 'uat'
    except:
        ENV_TYPE = "TEST"
ENV_TYPE = ENV_TYPE.upper() if ENV_TYPE else "TEST"
CC_TO_LOGIN_USER = ENV_TYPE != 'PROD' and (os.environ.get('CC_TO_LOGIN_USER') or 'false').lower() in ["true", "on", "1","yes","debug"]

