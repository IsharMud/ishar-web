"""
isharmud.com base views.
"""
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView

from ishar.apps.news.models import News


class ErrorView(TemplateView):
    """
    Template view for error handlers shows message with status code.
    """
    message = "Sorry, but unfortunately, there was an unknown error."
    status_code = 500
    template_name = "error.html"
    title = "Sorry!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["message"] = self.message
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=self.status_code)


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


class PortalView(TemplateView):
    """
    Portal view for logged-in users.
    """
    template_name = "portal.html"


class WelcomeView(TemplateView):
    """
    Main page.
    """
    template_name = "welcome.html"

    def get_context_data(self, **kwargs):
        """Include latest news post on main page."""
        context = super().get_context_data(**kwargs)
        context["news"] = News.objects.filter(
            is_visible=True
        ).order_by(
            "-created"
        ).first()
        return context
