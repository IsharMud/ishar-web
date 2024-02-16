"""
isharmud.com Django settings.
"""
from os import getenv
from pathlib import Path
from pymysql import install_as_MySQLdb
from django.core.management.utils import get_random_secret_key


# Set up MySQL.
install_as_MySQLdb()

# Build project path(s).
BASE_DIR = Path(__file__).resolve().parent

# Django secret key and REST API token for django-ninja.
REST_TOKEN = getenv("DJANGO_REST_TOKEN") or get_random_secret_key()
SECRET_KEY = getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# Debug.
DEBUG = bool(getenv("DJANGO_DEBUG", False))

# Allowed hosts.
DJANGO_HOSTS = getenv("DJANGO_HOSTS", "isharmud.com www.isharmud.com")
ALLOWED_HOSTS = DJANGO_HOSTS.split()

# Database(s).
DATABASES = {
    # Staging.
    "ishar_test": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ishar_test",
        "USER": "ishar_test",
        "PASSWORD": "SECRET",
        "HOST": "127.0.0.1",
        "PORT": 3306
    },
    # Production
    "ishar": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ishar",
        "USER": "ishar",
        "PASSWORD": "SECRET",
        "HOST": "127.0.0.1",
        "PORT": 3306
    }
}
DEFAULT_DB = getenv("DJANGO_DATABASE", "ishar")
DATABASES["default"] = DATABASES[DEFAULT_DB]

# Default primary key field type.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CSRF and session cookies.
CSRF_COOKIE_DOMAIN = SESSION_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
CSRF_COOKIE_HTTPONLY = SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE = True
DJANGO_ORIGINS = getenv(
    "DJANGO_ORIGINS",
    "https://isharmud.com https://www.isharmud.com"
)
CSRF_TRUSTED_ORIGINS = DJANGO_ORIGINS.split()

# E-mail.
ADMINS = MANAGERS = (("Administrator", "admin@" + ALLOWED_HOSTS[0]),)
DEFAULT_FROM_EMAIL = SERVER_EMAIL = "admin@" + ALLOWED_HOSTS[0]
EMAIL_SUBJECT_PREFIX = "[Django: " + ALLOWED_HOSTS[0] + "] "
EMAIL_HOST = "mail.example.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = EMAIL_HOST_PASSWORD = None

# Application definition
INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    # "django.contrib.flatpages",
    "django.contrib.staticfiles",
    "ninja",
    "ishar",
    "ishar.apps.accounts",
    "ishar.apps.challenges",
    "ishar.apps.classes",
    "ishar.apps.clients",
    "ishar.apps.discord",
    "ishar.apps.events",
    "ishar.apps.faqs",
    "ishar.apps.help",
    "ishar.apps.leaders",
    "ishar.apps.news",
    "ishar.apps.patches",
    "ishar.apps.players",
    "ishar.apps.quests",
    "ishar.apps.races",
    "ishar.apps.seasons",
    "ishar.apps.skills"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
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
                "ishar.contexts.global_event_count",
                "ishar.contexts.website_title",
            ],
            "libraries": {
                "ishar": "ishar.templatetags"
            }
        },
    },
]

WSGI_APPLICATION = "wsgi.application"

# Authentication.
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"}
]
AUTH_USER_MODEL = "accounts.Account"
AUTHENTICATION_BACKENDS = (
    "ishar.apps.accounts.backends.IsharUserAuthBackend",
)
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/portal/"
LOGOUT_URL = "/logout/"

# Website title.
WEBSITE_TITLE = f"Ishar MUD LOCAL (DB: {DATABASES['default']['NAME']})"

# Logging.
LOGGING_DIR = "logs/"
LOGGING_ROOT = Path(BASE_DIR, LOGGING_DIR)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "verbose": {
            "datefmt": "%Y-%m-%d %H:%M:%S %Z",
            "format": "{asctime} [{levelname}] {message}",
            "style": "{",
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "discord": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.FileHandler",
            "filename": Path(LOGGING_ROOT, "discord.log"),
            "formatter": "verbose",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "error_log": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": Path(LOGGING_ROOT, "errors.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "discord": {
            "handlers": ["console", "discord"],
            "level": "INFO",
        },
        "django": {
            "handlers": ["console", "mail_admins", "error_log"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Internationalization.
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_THOUSAND_SEPARATOR = True
USE_TZ = True

# Static.
STATIC_URL = "static/"
STATIC_ROOT = Path(BASE_DIR, STATIC_URL)

# Media.
MEDIA_URL = "media/"
MEDIA_ROOT = Path(BASE_DIR, MEDIA_URL)
PATCHES_URL = "patches/"

# Discord.
DISCORD = {
    "APPLICATION_ID": "EXAMPLE",
    "GUILD": "EXAMPLE",
    "PUBLIC_KEY": "EXAMPLE",
    "TOKEN": "SECRET",
    "URL": "https://discord.com/invite/VBmMXUpeve"
}

# MUD files.
MUD_HOME = getenv("DJANGO_MUD_HOME", "/home/ishar/ishar-mud")
MUD_HOME_PATH = Path(MUD_HOME)
MUD_LIB = Path(MUD_HOME, "lib")
HELPTAB = Path(MUD_LIB, "Misc/helptab")
MUD_PODIR = Path(MUD_LIB, "Podir")

# Player immortal levels/types.
IMMORTAL_LEVELS = (
    (26, "God"),
    (25, "Forger"),
    (24, "Eternal"),
    (23, "Artisan"),
    (22, "Immortal"),
    (21, "Consort"),
)

CONNECT_URL = "https://mudslinger.net/play/?host=%s&port=%i" % (
    ALLOWED_HOSTS[0], 23
)

X_FRAME_OPTIONS = "SAMEORIGIN"
