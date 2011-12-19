# Django settings for rbutton project.
import os, sys
DEBUG = True
TEMPLATE_DEBUG = DEBUG


SITE_URL = 'http://localhost:8000/'

ADMINS = (
    ('Mark Scrimshire', 'mark@healthca.mp'),
)

MANAGERS = ADMINS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DBPATH=os.path.join(BASE_DIR, 'db/db.db')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DBPATH,                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

MEDIASYNC = {
    'BACKEND': 'mediasync.backends.s3',
    'AWS_KEY': "AKIAIE5XDCZ5PNK4RGOQ",
    'AWS_SECRET': "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",
    'AWS_BUCKET': "statichive",
}
MEDIASYNC['SERVE_REMOTE'] = True

TEMPLATE_CONTEXT_PROCESSORS = ( 'django.core.context_processors.auth',
                                #for user template var
                                'django.core.context_processors.debug',
                                'django.core.context_processors.i18n',
                                'django.core.context_processors.media',
                                'django.core.context_processors.static',
                                #for MEDIA_URL template var
                                'django.core.context_processors.request',
                                # #includes request in RequestContext
                                'rbutton.apps.accounts.processors.display',
                               )

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

#django_rpx_plus static/default values
LOGIN_URL = '/janrain/login/'
LOGOUT_URL = '/janrain/logout/'
LOGIN_REDIRECT_URL = '/accounts/profile/'

REDIRECT_DONATE = '/'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
# Add django_rpx_plus backend before default ModelBackend
#                           'django_rpx_plus.backends.RpxBackend',
                            'rbutton.apps.janrain.backends.JanrainBackend',
                           'django.contrib.auth.backends.ModelBackend',
                           )
#logout after 10 minutes of inactivity
#SESSION_COOKIE_AGE=600
#logout if the browser is closed
#SESSION_EXPIRE_AT_BROWSER_CLOSE=True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://127.0.0.1:8000/media/'
MEDIA_URL = '/media/'
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"

STATIC_URL = '/static/'
# STATIC_URL = '/mainstatic/'

#STATIC_URL="https://statichive.s3.amazonaws.com/"
# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin'
ADMIN_MEDIA_PREFIX = 'https://cegdjadmin.s3.amazonaws.com/'
MAIN_STATIC_ROOT = os.path.join(BASE_DIR, 'mainstatic')
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    MAIN_STATIC_ROOT,
    '/users/mark/pycharmprojects/rbutton/mainstatic/'
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ap^2y646_s=_^yoz64df*uefz*-jzr^pkk=ls-st&fhny+inj0'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'rbutton.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'mediasync',
    #'south',
    'rbutton.apps.uploadblue',
    'rbutton.apps.accounts',
    'rbutton.apps.registry',
    'rbutton.apps.janrain',

#    'django_rpx_plus',

)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Twilio SMS Login Settings ---------------------------------------------------
TWILIO_DEFAULT_FROM="+12024992459"
TWILIO_API_BASE="https://api.twilio.com/2010-04-01"
TWILIO_SID= "AC4d3f4dcee199445c45faa797c5c97898"
TWILIO_AUTH_TOKEN="d623565a60e77bb5902e1971948c6f17"
TWILIO_API_VERSION='2010-04-01'
SMS_LOGIN_TIMEOUT_MIN=10


EMAIL_HOST = 'smtp.google.com'
EMAIL_PORT = 587 #25 by default
EMAIL_HOST_USER = 'no-reply@healthca.mp'
EMAIL_HOST_PASSWORD = 'mypassword'


ACCOUNT_ACTIVATION_DAYS = 2
RESTRICT_REG_DOMAIN_TO = None
# MIN_PASSWORD_LEN=8
MIN_PASSWORD_LEN=1
# fixed for simple quick testing
############################
# #django_rpx_plus settings:
#
#
# ############################
JANRAIN_RPX_API_KEY = '1a7aa6d61d31f5126f791338d481d75e8bf6bc9e'
RPXNOW_API_KEY = '1a7aa6d61d31f5126f791338d481d75e8bf6bc9e'

# not requested but added here as record
# http://rpxnow.com/relying_parties/vlink2me
RPXNOW_APP_ID = 'gcpbgjlehcfgfdelhjkj'

# The realm is the subdomain of rpxnow.com that you signed up under. It handles
# your HTTP callback. (eg. http://mysite.rpxnow.com implies that RPXNOW_REALM  is
# 'mysite'.
RPXNOW_REALM = 'vlink2me'

# (Optional)
#RPX_TRUSTED_PROVIDERS = ''

# (Optional)
# Sets the language of the sign-in interface for *ONLY* the popup and the embedded
# widget. For the valid language options, see the 'Sign-In Interface Localization'
# section of https://rpxnow.com/docs. If not specified, defaults to
# settings.LANGUAGE_CODE (which is usually 'en-us').
# NOTE: This setting will be overridden if request.LANGUAGE_CODE (set by django's
#       LocaleMiddleware) is set. django-rpx-plus does a best attempt at mapping
#       django's LANGUAGE_CODE to RPX's language_preference (using
#       helpers.django_lang_code_to_rpx_lang_preference).
#RPX_LANGUAGE_PREFERENCE = 'en'

# If it is the first time a user logs into your site through RPX, we will send
# them to a page so that they can register on your site. The purpose is to
# let the user choose a username (the one that RPX returns isn't always suitable)
# and confirm their email address (RPX doesn't always return the user's email).
REGISTER_URL = '/accounts/rpx_register/'


# fixed for simple quick testing
############################
# #janrain settings:
#
#
#############################
JANRAIN_RPX_API_KEY = '1a7aa6d61d31f5126f791338d481d75e8bf6bc9e'

USERID_PRIORITY = 'UID'

# Choose primary User_Id. default is UID, alternatives are 'preferredUsername' or 'email'
# Note email is not always available
# If email is chosen as USERID_PRIORITY and
# email is not available switch to preferredUsername as alternative
# this is to end up with friendlier user names than
# the 20+ character random UID sequence

CLEAN_USERNAME_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_@,.-'
