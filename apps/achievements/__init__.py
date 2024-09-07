from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AchievementsConfig(AppConfig):
    app_label = "achievements"
    name = "apps.achievements"
    verbose_name = _("Achievement")
    verbose_name_plural = _("Achievements")
