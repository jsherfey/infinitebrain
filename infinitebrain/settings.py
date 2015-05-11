"""
Django settings for infinitebrain project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

PROJECT_DIR = os.path.dirname(__file__)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#bzf+3ho^kr2rnnc_1iooav_7ven)@4k(ku94z&0!1o4ner-s6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

##################################################
# THE FOLLOWING LINES WERE ADDED FOR DEVELOPMENT:
if DEBUG:
    STATICFILES_DIRS = (
        os.path.join(PROJECT_DIR, 'static'),
    )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
##################################################



TEMPLATE_DEBUG = True
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    #'django_notify.context_processors.notifications',
    'sekizai.context_processors.sekizai',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
)
#TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
#    'django.core.context_processors.request',
#    'django.core.context_processors.i18n',
#    'sekizai.context_processors.sekizai',
#    'django.core.context_processors.debug',
#)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.comments',
    'haystack',
    'modeldb',
    'registration',
    'twitter_feed',
    'tweepy',
    'south',
    'taggit',
    'taggit_templatetags',
    'qhonuskan_votes',
    # # # # # # # # # ################
    # removed 'django-nyt'
    # ###############################
    'django_notify',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'wiki.plugins.images',
    'wiki.plugins.macros',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django_notify.middleware.NotificationsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'infinitebrain.urls'

WSGI_APPLICATION = 'infinitebrain.wsgi.application'

SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
    'django_nyt': 'django_nyt.south_migrations',
    'wiki': 'wiki.south_migrations',
    'images': 'wiki.plugins.images.south_migrations',
    'notifications': 'wiki.plugins.notifications.south_migrations',
    'attachments': 'wiki.plugins.attachments.south_migrations',
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if DEBUG:
    DATABASES = { 'default': {
         'ENGINE': 'django.db.backends.sqlite3',  # this just added for development
        'NAME': 'devdb',  # again, just added for development
        'USER': '',
        'PASSWORD': '',
        }
    }
else:
       DATABASES = { 'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'modulator',                  # Or path to database file if using sqlite3.
            'USER': 'dev',                      # Not used with sqlite3.
            'PASSWORD': 'l3rAInzRck',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

LOGIN_REDIRECT_URL = '/'

# Registration settings
ACCOUNT_ACTIVATION_DAYS=7
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'theinfinitebrain@gmail.com' 
EMAIL_HOST_PASSWORD = 'l3rAInzRck'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST='localhost'
#EMAIL_PORT=25#587 #"587" #25 # Port to use for the SMTP server

SITE_ID = 1

EMAIL_SUBJECT_PREFIX='[infinitebrain]'
#DEFAULT_FROM_EMAIL = 'jason@infinitebrain.org'
# dummy server: sudo python -m smtpd -n -c DebuggingServer localhost:1025

# Twitter settings
TWITTER_FEED_CONSUMER_PUBLIC_KEY = 'tWllmoyOjOi3T9ujUk7lH0M32'
TWITTER_FEED_CONSUMER_SECRET = '22T6k9UfXZ4op4Zw0JwHi2WHRHF2tgzlfYOHfjFPrIy4kmY0I4'
TWITTER_FEED_OPEN_AUTH_TOKEN = '2270834493-IcR5CNhh9YDpcpUM8KUGqylI6FokHbASdd9QCoa'
TWITTER_FEED_OPEN_AUTH_SECRET = 'lC9mi67oTzN0bIDmhhbx36JiqcZM4OPvuAPhjSMpG3mWh'

# HAYSTACK settings. Path is the location of the whoosh index.
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}