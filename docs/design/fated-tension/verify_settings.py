"""Verification-only settings: the real settings.py over sqlite, with the
game's helptab from the ishar-mud clone. Never used in production."""
from settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/tmp/claude-0/-home-user-ishar-web/f631e60d-2c23-527e-b7f0-18ab25133956/scratchpad/verify.sqlite3",
    }
}
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]
WEBSITE_TITLE = "Ishar MUD"
DEBUG = True
HELPTAB = "/home/user/ishar-mud/lib/Misc/helptab"
MUD_HOME = "/home/user/ishar-mud"
CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
          DJANGO_CACHE_KEY: {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
STORAGES["staticfiles"] = {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}

# sqlite has no unsigned auto-increment: fall back to Django's AutoField and
# make the project's UnsignedAutoField emit sqlite's spelling.
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
from apps.core.models.unsigned import UnsignedAutoField  # noqa: E402
UnsignedAutoField.db_type = lambda self, connection: "integer"
UnsignedAutoField.rel_db_type = lambda self, connection: "integer"

# No migration history on the throwaway sqlite file: syncdb creates the
# managed tables straight from the models.
MIGRATION_MODULES = {
    name.rsplit(".", 1)[-1].replace("Config", "").lower(): None
    for name in INSTALLED_APPS if name.startswith("apps.")
}
MIGRATION_MODULES.update({
    "feedback": None, "connect": None, "patches": None, "patchnotes": None,
    "news": None, "notes": None, "surveys": None, "trials": None, "events": None,
    "faqs": None, "clients": None, "history": None, "processes": None, "core": None,
})

MIDDLEWARE = [m for m in MIDDLEWARE if "cache" not in m] + ["autologin.AutoLoginMiddleware"]
INTERNAL_IPS = ["127.0.0.1"]
