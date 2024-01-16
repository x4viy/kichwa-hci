# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, environ
import socket

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env('SECRET_KEY', default='S#perS3crEt_007')
SECRET_KEY = 'django-insecure-vv5*7!y@s8-6!a9b=nom&ad*ng8o(1m26cj_vcj1x38mig^u4i'

# this is your "password/ENCRYPT_KEY"
ENCRYPT_KEY = b'ERPUDAv2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Assets Management
ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

# load production server from .env
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

ALLOWED_HOSTS = ['*', get_ip_address(),  'localhost', 'localhost:85', '127.0.0.1', env('SERVER', default='127.0.0.1')]
CSRF_TRUSTED_ORIGINS = ['http://localhost:85', 'http://127.0.0.1', 'https://' + env('SERVER', default='127.0.0.1')]
print('running on : ', get_ip_address() + ':8000/')

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',# Enable the inner home (home)
    'apps.sis',
    'apps.gen',
    'apps.clasificacion',
    # Plugins
    'crispy_forms',
    'bootstrap_datepicker_plus',
    'captcha',
    'ckeditor',

]
CRISPY_TEMPLATE_PACK = 'bootstrap4'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "/400/temas/"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/home/templates")  # ROOT dir for templates
TEMPLATE_DIR = os.path.join(CORE_DIR, "templates/")  # ROOT dir for templates

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
                'apps.context_processors.cfg_assets_root',
            ],
            'libraries': {
                'quichua_tags': 'templates.tags.custom_tags',
            },
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': "channels.layers.InMemoryChannelLayer"
    }
}
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# if os.environ.get('DB_ENGINE') and os.environ.get('DB_ENGINE') == "postgres":
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'quichua'),
        'USER': os.getenv('DB_USERNAME', 'postgres'),
        'PASSWORD': os.getenv('DB_PASS', '3434'),
        # 'PASSWORD': os.getenv('DB_PASS', 'Erp2k19'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        # 'HOST': os.getenv('DB_HOST', '172.16.1.77'),
        'PORT': os.getenv('DB_PORT', 5432),
    },
    'adm': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=adm'
        },
        'NAME': os.getenv('DB_NAME', 'quichua'),
        'USER': os.getenv('DB_USERNAME', 'postgres'),
        'PASSWORD': os.getenv('DB_PASS', '3434'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', 5432),
    },
    'gen': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=gen'
        },
        'NAME': os.getenv('DB_NAME', 'quichua'),
        'USER': os.getenv('DB_USERNAME', 'postgres'),
        'PASSWORD': os.getenv('DB_PASS', '3434'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', 5432),
    },
    'sis': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=sis'
        },
        'NAME': os.getenv('DB_NAME', 'quichua'),
        'USER': os.getenv('DB_USERNAME', 'postgres'),
        'PASSWORD': os.getenv('DB_PASS', '3434'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', 5432),
    },
}
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': 'db.sqlite3',
#         }
#     }

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

LANGUAGE_CODE = 'es-ec'

TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DATE_INPUT_FORMATS = ('%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y')

DATE_FORMAT = "d-m-Y"
#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "staticfiles")
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    # os.path.join(CORE_DIR, 'apps/../static'),
    os.path.join(CORE_DIR, 'static/'),
)

#############################################################
#############################################################

# For media files
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

#
LOGIN_URL = '/'

# for session expire
# SESSION_EXPIRE_SECONDS = 7200

# De forma predeterminada, la sesión caducará X segundos después del inicio de la sesión.
# Para caducar la sesión X segundos después de la last activity, use la siguiente configuración:
# SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

# De forma predeterminada, last activiy se agruparán por segundo. Para agrupar por diferentes períodos,
# use la siguiente configuración:
# SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60 # group by minute

# Para redirigir a una URL personalizada, defina la siguiente configuración:
SESSION_TIMEOUT_REDIRECT = '/'


RECAPTCHA_PUBLIC_KEY = '6LfQdJwnAAAAAK56nWNTefh3jecVyyrWpVme77BB'
RECAPTCHA_PRIVATE_KEY = '6LfQdJwnAAAAALAtxonM64CUY6k3r1oDe1dfy9va'

# Get local IP address