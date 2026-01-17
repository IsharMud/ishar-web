from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ConditionsConfig(AppConfig):
    app_label = "conditions"
    name = "apps.conditions"
    verbose_name = _("Condition")
    verbose_name_plural = _("Conditions")
