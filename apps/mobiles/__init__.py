from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MobilesConfig(AppConfig):
    app_label = "mobiles"
    name = "apps.mobiles"
    verbose_name = _("Mobile")
    verbose_name_plural = _("Mobiles")
