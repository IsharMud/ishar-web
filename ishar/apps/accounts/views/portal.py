from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class PortalView(LoginRequiredMixin, TemplateView):
    template_name = "portal.html"
