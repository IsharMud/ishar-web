"""isharmud.com Django settings."""
from os import getenv
from pathlib import Path
from pymysql import install_as_MySQLdb
from django.core.management.utils import get_random_secret_key


# Set up MySQL.
install_as_MySQLdb()

# Build project path(s).
BASE_DIR = Path(__file__).resolve().parent

# Django secret key.
SECRET_KEY = getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# Website title.
WEBSITE_TITLE = "Ishar MUD"

# Debug.
DEBUG = bool(getenv("DJANGO_DEBUG", False))

# Allowed hosts.
DJANGO_HOSTS = getenv("DJANGO_HOSTS", "isharmud.com www.isharmud.com")
ALLOWED_HOSTS = DJANGO_HOSTS.split()

# Database(s).
DATABASES = {
    # Staging.
    "ishar_test": {
        "ENGINE": "apps.core.backends",
        "NAME": "ishar_test",
        "USER": "ishar_test",
        "PASSWORD": "secret",
        "HOST": "127.0.0.1",
        "PORT": 3306
    },
    # Production
    "ishar": {
        "ENGINE": "apps.core.backends",
        "NAME": "ishar",
        "USER": "ishar",
        "PASSWORD": "secret",
        "HOST": "127.0.0.1",
        "PORT": 3306
    }
}
DEFAULT_DB = getenv("DJANGO_DATABASE", "ishar")
DATABASES["default"] = DATABASES[DEFAULT_DB]

# Default primary key field type.
DEFAULT_AUTO_FIELD = "apps.core.models.unsigned.UnsignedAutoField"

# CSRF and session cookies.
CSRF_COOKIE_DOMAIN = SESSION_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
CSRF_COOKIE_HTTPONLY = SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE = True
DJANGO_ORIGINS = getenv(
    "DJANGO_ORIGINS",
    "https://isharmud.com https://www.isharmud.com"
)
CSRF_TRUSTED_ORIGINS = DJANGO_ORIGINS.split()

# E-mail.
DEFAULT_FROM_EMAIL = SERVER_EMAIL = "admin@" + ALLOWED_HOSTS[0]
ADMINS = MANAGERS = (("Example", SERVER_EMAIL),)
EMAIL_SUBJECT_PREFIX = "[Django: " + WEBSITE_TITLE + "] "
EMAIL_HOST = "smtp.example.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = EMAIL_HOST_PASSWORD = None

# Application definition.
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "apps.CoreConfig",
    "apps.AccountsConfig",
    "apps.AchievementsConfig",
    "apps.ChallengesConfig",
    "apps.ClassesConfig",
    "apps.ClientsConfig",
    "apps.DiscordConfig",
    "apps.EventsConfig",
    "apps.FAQsConfig",
    "apps.HelpConfig",
    "apps.LeadersConfig",
    "apps.MobilesConfig",
    "apps.NewsConfig",
    "apps.ObjectsConfig",
    "apps.PatchesConfig",
    "apps.PlayersConfig",
    "apps.ProcessesConfig",
    "apps.QuestsConfig",
    "apps.RacesConfig",
    "apps.SeasonsConfig",
    "apps.SkillsConfig"
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
                "apps.core.contexts.website_title",
                "apps.events.contexts.global_event_count",
                "apps.players.contexts.player_search_form",
                "apps.seasons.contexts.current_season",
            ],
#            "libraries": {
#                "ishar": "apps.core.templatetags"
#            }
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
    "apps.accounts.backends.IsharUserAuthBackend",
)
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/portal/"
LOGOUT_URL = "/logout/"

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

MIN_IMMORTAL_LEVEL = min(IMMORTAL_LEVELS)[0]
MAX_IMMORTAL_LEVEL = max(IMMORTAL_LEVELS)[0]

CONNECT_URL = "https://mudslinger.net/play/?host=%s&port=%i" % (
    ALLOWED_HOSTS[0], 23
)

X_FRAME_OPTIONS = "SAMEORIGIN"

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": None,

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": None,

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": None,

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "images/logo.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "images/favicon.png",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "images/favicon.png",

    # Welcome text on the login screen
    "welcome_sign": "",

    # Copyright on the footer
    "copyright": "IsharMUD",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    "search_model": [
        "accounts.Account",
        "mobiles.Mobile",
        "objects.Object",
        "quests.Quest",
        "skills.Skill"
    ],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": "get_gravatar",

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        # {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Home",  "url": "admin:index"},

        # external url that opens in a new window (Permissions can be added)
        # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # model admin to link to (Permissions checked against model)
        # {"model": "accounts.Account"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        # {"app": "classes"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": WEBSITE_TITLE, "url": "index", "new_window": True},
        {"name": "Source Code", "url": "https://github.com/IsharMud/ishar-web/", "new_window": True},
        {"name": "Support Ishar MUD", "url": "support", "new_window": True},
        # {"model": "accounts.Account"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["accounts",],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        # "books": [{
        #     "name": "Make Messages",
        #     "url": "make_messages",
        #     "icon": "fas fa-comments",
        #     "permissions": ["books.view_book"]
        # }]
    },

    # Custom icons for side menu apps/models
    # See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {

        # accounts
        "accounts.Account": "fas fa-user",
        "accounts.AccountUpgrade": "fas fa-arrow-up",

        # achievements
        "achievements.Achievement": "fas fa-mountain",
        "achievements.AchievementClassRestrict": "fas fa-not-equal",
        "achievements.AchievementCriteria": "fas fa-table",
        "achievements.AchievementReward": "fas fa-award",
        "achievements.AchievementTrigger": "fas fa-stopwatch",

        # challenges
        "challenges.Challenge": "fas fa-award",

        # classes
        "classes": "fas fa-people-group",
        "classes.Class": "fas fa-user",
        "classes.ClassLevel": "fas fa-arrow-up",
        "classes.ClassRace": "fas fa-user",
        "classes.ClassSkill": "fas fa-brain",

        # (MUD) clients
        "clients.MUDClient": "fas fa-terminal",
        "clients.MUDClientCategory": "fas fa-folder",

        # core
        "core": "fas fa-flag",
        "core.PlayerFlag": "fas fa-flag",
        "core.AffectFlag": "fas fa-flag",
        "core.Title": "fas fa-tag",

        # events
        "events.GlobalEvent": "fas fa-calendar",

        # faqs
        "faqs.FAQ": "fas fa-question",

        # mobiles
        "mobiles": "fas fa-skull",
        "mobiles.Mobile": "fas fa-skull",

        # news
        "news": "fas fa-newspaper",
        "news.News": "fas fa-newspaper",

        # objects
        "objects": "fas fa-object-group",
        "objects.Object": "fas fa-object-group",
        "objects.ObjectAffectFlag": "fas fa-flag",
        "objects.ObjectExtra": "fas fa-diagram-project",
        "objects.ObjectFlag": "fas fa-flag",
        "objects.ObjectMod": "fas fa-vector-square",
        "objects.ObjectObjectMod": "fas fa-draw-polygon",
        "objects.ObjectWearableFlag": "fas fa-flag",

        # patches
        "patches": "fas fa-file-pdf",
        "patches.Patch": "fas fa-file-pdf",

        # processes
        "processes": "fas fa-microchip",
        "processes.MUDProcess": "fas fa-microchip",

        # players
        "players": "fas fa-users-cog",
        "players.Player": "fas fa-user",
        "players.Immortal": "fas fa-user-shield",
        "players.RemortUpgrade": "fas fa-arrow-up",

        # quests
        "quests.Quest": "fas fa-mountain",
        "quests.QuestReward": "fas fa-award",

        # races
        "races": "fas fa-people",
        "races.Race": "fas fa-user",
        "races.RaceAffinity": "fas fa-brain",

        # season
        "seasons.Season": "fas fa-tree",

        # sites
        "django.contrib.sites": "fas fa-sitemap",

        # skills
        "skills.SpellFlag": "fas fa-flag",
        "skills.Force": "fas fa-infinity",
        "skills.Skill": "fas fa-brain",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cerulean",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
