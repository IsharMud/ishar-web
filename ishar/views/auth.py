from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView


class IsharLoginView(LoginView):
    """
    Log-in page.
    """
    template_name = "login.html"


class IsharLogoutView(LogoutView):
    """
    Log-out page.
    """
    template_name = "welcome.html"

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have logged out!")
        return super().dispatch(request, *args, **kwargs)
