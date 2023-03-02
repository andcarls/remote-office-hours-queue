"""
Django settings for officehours project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

import dj_database_url


def csv_to_list(csv, delim=','):
    try:
        return [x.strip() for x in csv.split(delim) if x.strip()]
    except Exception:
        return []


def str_to_bool(val):
    return val.lower().strip() in ('yes', 'true', 'on', '1')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '_c8d6tdowj2bb50^t&kb)o3o-+oi!n0n@y+ik%#ty1-nd89uug')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str_to_bool(os.getenv('DEBUG', 'off'))

ALLOWED_HOSTS = csv_to_list(os.getenv('ALLOWED_HOSTS', None))


# Application definition

# Add additional non-Django apps here for consistent logging behavior
EXTRA_APPS = [
    'daphne',
    'channels',
    'officehours_api.apps.OfficehoursApiConfig',
    'officehours_ui.apps.OfficehoursUiConfig',
]

INSTALLED_APPS = [
    *EXTRA_APPS,
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'safedelete',
    'watchman',
    'webpack_loader',
    'rest_framework_tracking',
    'django_filters',
    'django.contrib.sites',
    'django.contrib.flatpages',
]

if DEBUG:
    INSTALLED_APPS += [
        'drf_spectacular',
    ]

WATCHMAN_TOKENS = os.getenv('WATCHMAN_TOKENS')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

OIDC_RP_CLIENT_ID = os.getenv('OIDC_RP_CLIENT_ID')
OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_RP_CLIENT_SECRET')
OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv('OIDC_OP_AUTHORIZATION_ENDPOINT')
OIDC_OP_TOKEN_ENDPOINT = os.getenv('OIDC_OP_TOKEN_ENDPOINT')
OIDC_OP_USER_ENDPOINT = os.getenv('OIDC_OP_USER_ENDPOINT')
OIDC_RP_SIGN_ALGO = os.getenv('OIDC_RP_SIGN_ALGO', 'RS256')
OIDC_OP_JWKS_ENDPOINT = os.getenv('OIDC_OP_JWKS_ENDPOINT')
OIDC_USERNAME_ALGO = 'officehours.auth.generate_username'
OIDC_RP_SCOPES = 'openid email profile'
OIDC_CREATE_USER = str_to_bool(os.getenv('OIDC_CREATE_USER', 'on'))

if (OIDC_RP_CLIENT_ID and OIDC_RP_CLIENT_SECRET and OIDC_OP_AUTHORIZATION_ENDPOINT
        and OIDC_OP_TOKEN_ENDPOINT and OIDC_OP_USER_ENDPOINT):
    INSTALLED_APPS += ['mozilla_django_oidc']
    AUTHENTICATION_BACKENDS += ['officehours.auth.UMichOIDCBackend']
    LOGIN_URL = '/oidc/authenticate/'
else:
    print('Skipping OIDCAuthenticationBackend as OIDC variables were not set.')

# Work around OpenShift TLS Termination
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Django Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'officehours_api.exceptions.backend_error_handler',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'redirect_to_non_www.middleware.RedirectToNonWww',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'officehours.urls'

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
                'officehours_ui.context_processors.feedback',
                'officehours_ui.context_processors.debug',
                'officehours_ui.context_processors.login_url',
                'officehours_ui.context_processors.spa_globals',
            ],
        },
    },
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'dist/',
        'IGNORE': [r'.+\.hot-update.js']
    }
}

WSGI_APPLICATION = 'officehours.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {}
DATABASES['default'] = dj_database_url.config(default='sqlite:///db.sqlite3')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.getenv('DJANGO_TIMEZONE', 'America/Detroit')

USE_I18N = True

USE_L10N = True

USE_TZ = True


def skip_auth_callback_requests(record):
    if record.getMessage().startswith('HTTP GET /callback/'):
        return False
    return True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {message}',
            'style': '{'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'skip_auth_callback_requests': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_auth_callback_requests,
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['skip_auth_callback_requests'],
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console', 'mail_admins'],
            'propagate': True,
        },
        'mozilla_django_oidc': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        **{
            app.split('.')[0]: {
                'level': 'DEBUG' if DEBUG else 'INFO',
                'handlers': ['console', 'mail_admins'],
                'propagate': False
            } for app in EXTRA_APPS
        }
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

FEEDBACK_EMAIL = os.getenv('FEEDBACK_EMAIL')


# safedelete
SAFE_DELETE_INTERPRET_UNDELETED_OBJECTS_AS_CREATED = True


# drf-api-tracking
DRF_TRACKING_ADMIN_LOG_READONLY = True
LOGGING_METHODS = csv_to_list(
    os.getenv('LOGGING_METHODS', 'POST, PUT, PATCH, DELETE')
)


# Email
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_SUBJECT_PREFIX = os.getenv('EMAIL_SUBJECT_PREFIX', '[ROHQ] ')

ADMINS = [('Admins', os.getenv('ADMIN_EMAIL'))]
MANAGERS = ADMINS


# Google Analytics
GA_TRACKING_ID = os.getenv('GA_TRACKING_ID')

# Django Flatpages
SITE_ID = 1

# Channels
ASGI_APPLICATION = 'officehours.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(
                os.getenv('REDIS_HOST', 'redis'),
                int(os.getenv('REDIS_PORT', '6379'))
            )],
        },
    },
}

# Notifications
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_MESSAGING_SERVICE_SID = os.getenv('TWILIO_MESSAGING_SERVICE_SID')

# Backends
DOCS_BASE_URL = 'https://its.umich.edu/communication/videoconferencing/'

ZOOM_DOCS_URL = os.getenv('ZOOM_DOCS_URL', DOCS_BASE_URL + 'zoom/getting-started')
ZOOM_BASE_DOMAIN_URL = os.getenv('ZOOM_BASE_DOMAIN_URL', 'https://umich.zoom.us')
ZOOM_PROFILE_URL = os.getenv('ZOOM_PROFILE_URL', ZOOM_BASE_DOMAIN_URL + '/profile')
ZOOM_INTL_URL = os.getenv('ZOOM_INTL_URL', ZOOM_PROFILE_URL + '/setting?tab=telephony')
ZOOM_TELE_NUM = os.getenv('ZOOM_TELE_NUM', '1.312.626.6799')
ZOOM_SIGN_IN_HELP = os.getenv('ZOOM_SIGN_IN_HELP')

BLUEJEANS_DOCS_URL = os.getenv('BLUEJEANS_DOCS_URL', DOCS_BASE_URL + 'blue-jeans/getting-started')
BLUEJEANS_TELE_NUM = os.getenv('BLUEJEANS_TELE_NUM', '1.312.216.0325')
BLUEJEANS_INTL_URL = os.getenv('BLUEJEANS_INTL_URL', 'https://www.bluejeans.com/premium-numbers')

ENABLED_BACKENDS = {'inperson'}
DEFAULT_BACKEND = "inperson"

BLUEJEANS_CLIENT_ID = os.getenv('BLUEJEANS_CLIENT_ID', '').strip()
BLUEJEANS_CLIENT_SECRET = os.getenv('BLUEJEANS_CLIENT_SECRET', '').strip()
if BLUEJEANS_CLIENT_ID and BLUEJEANS_CLIENT_SECRET:
    ENABLED_BACKENDS.add("bluejeans")
    DEFAULT_BACKEND = "bluejeans"

ZOOM_CLIENT_ID = os.getenv('ZOOM_CLIENT_ID', '').strip()
ZOOM_CLIENT_SECRET = os.getenv('ZOOM_CLIENT_SECRET', '').strip()
if ZOOM_CLIENT_ID and ZOOM_CLIENT_SECRET:
    ENABLED_BACKENDS.add("zoom")
    DEFAULT_BACKEND = "zoom"

DEFAULT_ALLOWED_BACKENDS = (
    csv_to_list(os.getenv('DEFAULT_ALLOWED_BACKENDS'))
    if os.getenv('DEFAULT_ALLOWED_BACKENDS', None)
    else [DEFAULT_BACKEND]
)
