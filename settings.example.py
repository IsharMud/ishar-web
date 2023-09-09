"""
isharmud.com Django settings.
"""
from pathlib import Path
import pymysql


pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "SECRET"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["django.isharmud.com"]

# SECURITY WARNING: do not share your Discord secrets
DISCORD = {
    "APPLICATION_ID": "EXAMPLE",
    "GUILD": "EXAMPLE",
    "PUBLIC_KEY": "EXAMPLE",
    "TOKEN": "SECRET.SECRET.SECRET",
    "URL": "https://discord.com/invite/EXAMPLE"
}

# SECURITY WARNING: do not share your Sentry secret(s)
SENTRY_DSN = "SECRET"

# MUD home and lib directory, for "helptab" file reading and player "Podir"s
MUD_HOME = Path("/home/ishar/ishar-mud")
MUD_LIB = Path(MUD_HOME, "lib")
HELPTAB = Path(MUD_LIB, "Misc/helptab")
MUD_PODIR = Path(MUD_LIB, "Podir")

# Player karma alignment ranges
ALIGNMENTS = {
    "Very Evil": (-1500, -1000),
    "Evil": (-1000, -500),
    "Slightly Evil": (-500, -250),
    "Neutral": (-250, 250),
    "Slightly Good": (250, 500),
    "Good": (500, 1000),
    "Very Good": (1000, 1500)
}

# Player game types
GAME_TYPES = [
    (0, "Classic"),
    (1, "Survival")
]

# Player immortal levels/types
IMMORTAL_LEVELS = (
    (26, "God"),
    (25, "Forger"),
    (24, "Eternal"),
    (23, "Artisan"),
    (22, "Immortal"),
    (21, "Consort"),
)

# Authentication using MySQL database user accounts
AUTH_USER_MODEL = "accounts.Account"
AUTHENTICATION_BACKENDS = (("ishar.backends.IsharUserAuthBackend"),)

# CSRF/session cookies
CSRF_COOKIE_DOMAIN = SESSION_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
CSRF_COOKIE_HTTPONLY = CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = SESSION_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_HTTPONLY = SESSION_COOKIE_SECURE = True


# E-mail
ADMINS = MANAGERS = (("Eric OC", "eric@ericoc.com"),)
DEFAULT_FROM_EMAIL = "django@" + ALLOWED_HOSTS[0]
EMAIL_SUBJECT_PREFIX = "[Django: " + ALLOWED_HOSTS[0] + "] "
SERVER_EMAIL = "admin@" + ALLOWED_HOSTS[0]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "ishar",
    "ishar.apps.accounts",
    "ishar.apps.challenges",
    "ishar.apps.events",
    "ishar.apps.help",
    "ishar.apps.leaders",
    "ishar.apps.news",
    "ishar.apps.patches",
    "ishar.apps.players",
    "ishar.apps.quests",
    "ishar.apps.seasons",
    "ishar.apps.spells",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            Path(BASE_DIR, "ishar/templates/base")
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "ishar.contexts.current_season",
                "ishar.contexts.global_event_count"
            ],
        },
    },
]

WSGI_APPLICATION = "wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ishar",
        "USER": "ishar",
        "PASSWORD": "SECRET",
        "HOST": "127.0.0.1",
        "PORT": 3306
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"}
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# REST Framework API
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication"
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ]
}

# Static files (CSS, JavaScript, images)
STATIC_URL = "static/"
STATIC_ROOT = Path(BASE_DIR, STATIC_URL)

# Media (for patch PDF files)
MEDIA_URL = "media/"
MEDIA_ROOT = Path(BASE_DIR, MEDIA_URL)

USE_THOUSAND_SEPARATOR = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/portal/login/"
LOGIN_REDIRECT_URL = "/portal/"
LOGOUT_URL = "/portal/logout/"

CONNECT_HOST = ALLOWED_HOSTS[0]
CONNECT_PORT = "23"
CONNECT_URL = (
    "https://mudslinger.net/play/?host=" +
    ALLOWED_HOSTS[0] + "&port=" + CONNECT_PORT
)
