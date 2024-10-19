from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from apps.core.views.mixins import NeverCacheMixin


class PasswordView(LoginRequiredMixin, NeverCacheMixin, PasswordChangeView):
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = "password.html"
