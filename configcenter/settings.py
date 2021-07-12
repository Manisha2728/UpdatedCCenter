

# Django settings for configcenter project.
from . import params

# looking for the <key> arg as a variable.
# 1. try to retrieve from params.py - which holds dbMotion parameters 
# 2. use the retrieved value as a default when trying to read from locals.py
def get_param(key, default = None):
    default = getattr(params, key, default)
    
    try:
        from . import locals
    except ImportError:
        return default
    
    return getattr(locals, key, default)

DEBUG = get_param('debug', False)
TEMPLATE_DEBUG = DEBUG
VERSION = '21.3' #21.2 CU1
IS_MAJOR = True     # Major is not a CU, SP, PR, HF.

import os.path
PROJECT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
DBM_SHARED_FOLDER = get_param('dbm_shared_folder')


ADMINS = ()
LOGIN_URL = "/admin/login/"

MANAGERS = ADMINS

#AUTHENTICATION_BACKENDS = ('authccenter.backends.OfflineAuthenticationBackend.Backend','authccenter.backends.dbmAuthenticationBackend.Backend',)

DATABASES = {
        
	'default': {
      'NAME': get_param('db_name', 'dbmCCenter'),
      'ENGINE': 'sql_server.pyodbc',
        'HOST': get_param('db_host'),
        'OPTIONS': {
                    'provider': 'SQLNCLI11',
                   'use_mars': True,
                   'use_legacy_date_fields': True,
                    },
    },
    'cag_db': {
      'NAME': get_param('cag_db_name','dbmClinicalAnalyticsGateway'),
      'ENGINE': 'sql_server.pyodbc',
        'HOST': get_param('cag_sql_server_name'),
        'OPTIONS': {
                    'provider': 'SQLNCLI11',
                   'use_mars': True,
                   'use_legacy_date_fields': True,
                    },
    }

#     'default': {
#      'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#      'NAME': os.path.join(PROJECT_DIR, 'sqlite.db'),                      # Or path to database file if using sqlite3.
#      }

}

def _get_ccenter_shared_folder(create=False):
    _dir = os.path.realpath(os.path.join(DBM_SHARED_FOLDER, 'Services/CCenter'))
    if create:
        if not os.path.exists(_dir):
            os.makedirs(_dir)
    return _dir

def _get_hf_dir(create=False):
    hf_dir = os.path.join(_get_ccenter_shared_folder(False), 'HF')
    if create:
        if not os.path.exists(hf_dir):
            os.makedirs(hf_dir)
    return hf_dir

HF_DIR = _get_hf_dir(True)
CCENTER_SHARED_FOLDER = _get_ccenter_shared_folder(True)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

DBS_OPTIONS = {
    'table': 'dbmconfigapp_dbfiles',
    'base_url': '/dbmconfigapp/files/',
}

# Default url, handled in urls.py
LOGIN_REDIRECT_URL = '/'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, '../static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
     os.path.join(PROJECT_DIR, 'static'),
    #os.path.join(PROJECT_DIR, 'templates/admin'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
     'django.contrib.staticfiles.finders.FileSystemFinder',
     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!8^*mle4mocxzsxe38h3262nc$d1t*%ie2odekt1_y5@3!z(!h'


MIDDLEWARE = (
    'security.middleware.NoCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'authccenter.middleware.ConcurentSessionMiddleware',
)

ROOT_URLCONF = 'configcenter.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'configcenter.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'authccenter','templates'),

    os.path.join(PROJECT_DIR, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',

    'authccenter',
    'dbmconfigapp',
    'externalapps',
    'federation',
    'via',
    'security',
	'dataloading',
    
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Uncomment the next line to enable the admin:
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
] + get_param('INSTALLED_APPS', [])

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'default': {
            'format': 'Timestamp: %(asctime)s \n Log Level: %(levelname)s \n Component: %(name)s \n %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_DIR, 'error.log'),
            'formatter': 'default',
            'maxBytes': 1024,
            'backupCount': 3
        },
        # Log to dbMotion CCenter event log
        'eventlog': {
            'class': 'logging.handlers.NTEventLogHandler',
            'appname': 'dbMotion.CCenter',
            'logtype': 'dbMotion CCenter',
            'formatter': 'default',
        }
    },
    'loggers': {
        #'django.request': {
        #    'handlers': ['mail_admins'],
        #    'level': 'ERROR',
        #    'propagate': True,
        #},
        
        # log any django errors to the event log
        'django': {
            'handlers': ['eventlog'],
            'level': 'WARNING',
            'propagate': True
        },
    }
}


# Close the session when user closes the browser
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Set session timeout in sec (30 min)
SESSION_COOKIE_AGE = 1800
SESSION_SAVE_EVERY_REQUEST = True

TEST_RUNNER = "configcenter.test_runner.TestRunner"


