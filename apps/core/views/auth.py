from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView

from .mixins import NeverCacheMixin


class IsharLoginView(NeverCacheMixin, LoginView):
    """Log-in page."""
    template_name = "login.html"


class IsharLogoutView(NeverCacheMixin, LogoutView):
    """Log-out page."""
    next_page = "/"

    def dispatch(self, request, *args, **kwargs):
        messages.success(request=request, message="You have logged out!")
        return super().dispatch(request, *args, **kwargs)
