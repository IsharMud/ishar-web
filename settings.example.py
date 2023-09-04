"""
Django settings for isharmud.com project.
"""
from pathlib import Path
import pymysql


pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SECRET'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['isharmud.com', '127.0.0.1', 'localhost']

# SECURITY WARNING: do not share your Discord secrets
DISCORD = {
    "APPLICATION_ID": "EXAMPLE",
    "GUILD": "EXAMPLE",
    "PUBLIC_KEY": "EXAMPLE",
    "TOKEN": "SECRET.SECRET.SECRET",
    "URL": "https://discord.com/invite/EXAMPLE"
}

# SECURITY WARNING: do not share your Sentry secret(s)
SENTRY_DSN = 'https://SECRET@SECRET.ingest.sentry.io/SECRET'

# MUD home and lib directory, for "helptab" file reading and player "Podir"s
MUD_HOME = Path('/home/isharmud/isharmud')
MUD_LIB = Path(MUD_HOME, 'lib')
HELPTAB = Path(MUD_LIB, 'Misc/helptab')
MUD_PODIR = Path(MUD_LIB, 'Podir')

# Player karma alignment ranges
ALIGNMENTS = {
    'Very Evil': (-1500, -1000),
    'Evil': (-1000, -500),
    'Slightly Evil': (-500, -250),
    'Neutral': (-250, 250),
    'Slightly Good': (250, 500),
    'Good': (500, 1000),
    'Very Good': (1000, 1500)
}

# Player game types
GAME_TYPES = [
    (0, 'Classic'),
    (1, 'Survival')
]

# Player immortal levels
IMMORTAL_LEVELS = {
    26: 'God',
    25: 'Forger',
    24: 'Eternal',
    23: 'Artisan',
    22: 'Immortal',
    21: 'Consort'
}

# Authentication using MySQL database user accounts
AUTH_USER_MODEL = 'isharweb.Account'
AUTHENTICATION_BACKENDS = (
    ('django.contrib.auth.backends.ModelBackend'),
)

# CSRF cookie
CSRF_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SECURE = True

# E-mail
ADMINS = MANAGERS = (
    ("Example", "example@example.com"),
)
DEFAULT_FROM_EMAIL = "django@" + ALLOWED_HOSTS[0]
EMAIL_SUBJECT_PREFIX = "[Django: " + ALLOWED_HOSTS[0] + "] "
SERVER_EMAIL = "admin@" + ALLOWED_HOSTS[0]

# Session cookie
SESSION_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "ishar",
    "ishar.apps.account",
    "ishar.apps.challenge",
    "ishar.apps.news",
    "ishar.apps.player",
    "ishar.apps.quest",
    "ishar.apps.race",
    "ishar.apps.season",
    "ishar.apps.spell",
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

ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            Path(BASE_DIR, 'ishar/templates/base')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ishar.contexts.current_season',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# Database
DATABASES = {
    "default": {
        'ENGINE': "django.db.backends.mysql",
        'NAME': 'ishar',
        'USER': 'ishar',
        'PASSWORD': 'SECRET',
        'HOST': '127.0.0.1',
        'PORT': 3306
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = Path(BASE_DIR, STATIC_URL)

# Patch PDF folder
PATCH_DIR = Path(STATIC_ROOT, 'patches')

USE_THOUSAND_SEPARATOR = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "/admin/login/"
CONNECT_HOST = ALLOWED_HOSTS[0]
CONNECT_PORT = "23"
CONNECT_URL = (
    "https://mudslinger.net/play/?host=" +
    ALLOWED_HOSTS[0] + "&port=" + CONNECT_PORT
)
