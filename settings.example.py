"""
isharmud.com Django settings.
"""
from os import getenv
from pathlib import Path
from pymysql import install_as_MySQLdb
from django.core.management.utils import get_random_secret_key


# Set up MySQL.
install_as_MySQLdb()

# Silence OneToOneField recommendation warnings.
SILENCED_SYSTEM_CHECKS = ["fields.W342"]

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

# CSRF cookie.
CSRF_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SECURE = True
DJANGO_ORIGINS = getenv(
    "DJANGO_ORIGINS",
    "https://isharmud.com https://www.isharmud.com"
)
CSRF_TRUSTED_ORIGINS = DJANGO_ORIGINS.split()

# Language cookie.
LANGUAGE_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
LANGUAGE_COOKIE_HTTPONLY = True
LANGUAGE_COOKIE_SAMESITE = "Strict"
LANGUAGE_COOKIE_SECURE = True

# Session cookie.
SESSION_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SECURE = True

# Internationalization.
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_THOUSAND_SEPARATOR = True
USE_TZ = True

# E-mail.
ADMINS = MANAGERS = (("Example Person", "person@example.com"),)
DEFAULT_FROM_EMAIL = SERVER_EMAIL = "admin@" + ALLOWED_HOSTS[0]
EMAIL_SUBJECT_PREFIX = "[Django: " + ALLOWED_HOSTS[0] + "] "
EMAIL_HOST = "localhost"
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
WEBSITE_TITLE = "Ishar MUD"

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

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
    "PUBLIC_KEY":
    "EXAMPLE",
    "TOKEN":
    "SECRET",
    "URL": "https://discord.com/invite/VBmMXUpeve"
}

# MUD files.
MUD_HOME = Path(getenv("DJANGO_MUD_HOME", "/home/ishar/ishar-mud"))
MUD_LIB = Path(MUD_HOME, "lib")
HELPTAB = Path(MUD_LIB, "Misc/helptab")
MUD_PODIR = Path(MUD_LIB, "Podir")

# Player alignments.
ALIGNMENTS = {
    "Very Evil": (-1500, -1000),
    "Evil": (-1000, -500),
    "Slightly Evil": (-500, -250),
    "Neutral": (-250, 250),
    "Slightly Good": (250, 500),
    "Good": (500, 1000),
    "Very Good": (1000, 1500)
}

# Player game types.
GAME_TYPES = [(0, "Classic"), (1, "Survival")]

# Player immortal levels/types.
IMMORTAL_LEVELS = (
    (26, "God"),
    (25, "Forger"),
    (24, "Eternal"),
    (23, "Artisan"),
    (22, "Immortal"),
    (21, "Consort"),
)

# Player genders.
PLAYER_GENDERS = ((1, "Male"), (2, "Female"))

# Player positions.
PLAYER_POSITIONS = (
    (0, "POSITION_DEAD"), (1, "POSITION_DYING"), (2, "POSITION_STUNNED"),
    (3, "POSITION_PARALYZED"), (4, "POSITION_SLEEPING"),
    (5, "POSITION_HOISTED"), (6, "POSITION_RESTING"), (7, "POSITION_SITTING"),
    (8, "POSITION_RIDING"), (9, "UNUSED_POSN"), (10, "POSITION_STANDING")
)

# Order statistics by class.
CLASS_STATS = {
    "Warrior": (
        "Strength", "Agility", "Endurance", "Willpower", "Focus", "Perception"
    ),
    "Rogue": (
        "Agility", "Perception", "Strength", "Focus", "Endurance", "Willpower"
    ),
    "Cleric": (
        "Willpower", "Strength", "Perception", "Endurance", "Focus", "Agility"
    ),
    "Magician": (
        "Perception", "Focus", "Agility", "Willpower", "Endurance", "Strength"
    ),
    "Necromancer": (
        "Focus", "Willpower", "Perception", "Agility", "Strength", "Endurance"
    ),
    "Shaman": (
        "Willpower", "Agility", "Endurance", "Focus", "Perception", "Strength",
    ),
    # Alphabetic as last resort
    None: (
        "Agility", "Endurance", "Focus", "Perception", "Strength", "Willpower"
    )
}

CONNECT_URL = "https://mudslinger.net/play/?host=%s&port=%i" % (
    ALLOWED_HOSTS[0], 23
)

X_FRAME_OPTIONS = "SAMEORIGIN"
