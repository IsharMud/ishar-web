"""
isharmud.com base views.
"""
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView

from ishar.apps.news.models import News


class IsharLoginView(LoginView):
    template_name = "login.html.djt"


class IsharLogoutView(LogoutView):
    template_name = "welcome.html.djt"

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have logged out!")
        return super().dispatch(request, *args, **kwargs)


class PortalView(TemplateView):
    template_name = "portal.html.djt"


class WelcomeView(TemplateView):
    """
    Main page.
    """
    template_name = "welcome.html.djt"

    def get_context_data(self, **kwargs):
        """
        Add news to the main page.
        """
        context = super().get_context_data(**kwargs)
        context["news"] = News.objects.filter(
            is_visible=True
        ).order_by(
            "-created"
        ).first()
        return context
