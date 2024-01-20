"""
isharmud.com Django settings.
"""
from pathlib import Path
import pymysql


pymysql.install_as_MySQLdb()

# Set website title.
WEBSITE_TITLE = "Ishar MUD"

# Silence OneToOneField warnings.
SILENCED_SYSTEM_CHECKS = ["fields.W342"]
"""
System check identified some issues:

WARNINGS:
accounts.AccountAccountUpgrade.account: (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a OneToOneField.
        HINT: ForeignKey(unique=True) is usually better served by a OneToOneField.
players.PlayerRemortUpgrade.player: (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a OneToOneField.
        HINT: ForeignKey(unique=True) is usually better served by a OneToOneField.
players.PlayersFlag.flag: (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a OneToOneField.
        HINT: ForeignKey(unique=True) is usually better served by a OneToOneField.
"""

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: keep the secret key used in production secret!
REST_TOKEN = "SECRET"
SECRET_KEY = "SECRET"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ("isharmud.com", "www.isharmud.com")

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

# Player gender values
PLAYER_GENDERS = ((1, "Male"), (2, "Female"))

# Player position values
PLAYER_POSITIONS = (
    (0, "POSITION_DEAD"), (1, "POSITION_DYING"), (2, "POSITION_STUNNED"),
    (3, "POSITION_PARALYZED"), (4, "POSITION_SLEEPING"),
    (5, "POSITION_HOISTED"), (6, "POSITION_RESTING"), (7, "POSITION_SITTING"),
    (8, "POSITION_RIDING"), (9, "UNUSED_POSN"), (10, "POSITION_STANDING")
)

# Authentication using MySQL database user accounts
AUTH_USER_MODEL = "accounts.Account"
AUTHENTICATION_BACKENDS = (
    "ishar.apps.accounts.backends.IsharUserAuthBackend",
)

# Order of character statistics based on player class
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

# CSRF/session cookies
CSRF_COOKIE_DOMAIN = SESSION_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
CSRF_COOKIE_HTTPONLY = CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = SESSION_COOKIE_SAMESITE = "Strict"
CSRF_TRUSTED_ORIGINS = ("https://isharmud.com", "https://www.isharmud.com")
SESSION_COOKIE_HTTPONLY = SESSION_COOKIE_SECURE = True


# E-mail
ADMINS = MANAGERS = (("Eric OC", "eric@ericoc.com"),)
DEFAULT_FROM_EMAIL = "django@" + ALLOWED_HOSTS[0]
EMAIL_SUBJECT_PREFIX = "[Django: " + ALLOWED_HOSTS[0] + "] "
SERVER_EMAIL = "admin@" + ALLOWED_HOSTS[0]

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
    "django.contrib.flatpages",
    "django.contrib.staticfiles",
    "ninja",
    "ishar",
    "ishar.apps.accounts",
    "ishar.apps.challenges",
    "ishar.apps.classes",
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

# Static files (CSS, JavaScript, images)
STATIC_URL = "static/"
STATIC_ROOT = Path(BASE_DIR, STATIC_URL)

# Media (for patch PDF files)
MEDIA_URL = "media/"
MEDIA_ROOT = Path(BASE_DIR, MEDIA_URL)

USE_THOUSAND_SEPARATOR = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/portal/"
LOGOUT_URL = "/logout/"

CONNECT_HOST = ALLOWED_HOSTS[0]
CONNECT_PORT = 23
CONNECT_URL = (
    f"https://mudslinger.net/play/?host={CONNECT_HOST}&port={CONNECT_PORT}"
)
