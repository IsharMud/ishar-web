from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from apps.core.views.mixins import NeverCacheMixin


class PortalView(LoginRequiredMixin, NeverCacheMixin, TemplateView):
    template_name = "portal.html"
