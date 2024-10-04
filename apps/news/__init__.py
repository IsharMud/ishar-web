from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NewsConfig(AppConfig):
    app_label = "news"
    name = "apps.news"
    verbose_name = verbose_name_plural = _("News")
