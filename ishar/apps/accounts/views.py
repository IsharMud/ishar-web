from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.base import TemplateView


class PortalView(LoginRequiredMixin, TemplateView):
    template_name = "portal.html"


class PasswordView(LoginRequiredMixin, PasswordChangeView):
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = "password.html"
