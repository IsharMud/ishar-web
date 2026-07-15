from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PatchNotesConfig(AppConfig):
    app_label = "patchnotes"
    name = "apps.patchnotes"
    verbose_name = verbose_name_plural = _("Patch Notes")
