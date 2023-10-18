"""
isharmud.com base views.
"""
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView

from ishar.apps.news.models import News


class ErrorView(TemplateView):
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


class Error400BadRequestView(ErrorView):
    """400 Bad Request."""
    status_code = 400
    title = "Bad Request"
    message = "Sorry, but the request was not understood."


class Error401NotAuthorizedView(ErrorView):
    """401 Not Authorized."""
    status_code = 401
    title = "Not Authorized"
    message = "Sorry, but you do not have authorization to access this page."


class Error403ForbiddenView(ErrorView):
    """403 Forbidden."""
    status_code = 403
    title = "Forbidden"
    message = "Sorry, but access to this location is forbidden."


class Error404PageNotFoundView(ErrorView):
    """404 Page Not Found."""
    status_code = 404
    title = "Page Not Found"
    message = "Sorry, but the page that you are looking for could not be found."


class Error405MethodNotAllowedView(ErrorView):
    """405 Method Not Allowed."""
    status_code = 405
    title = "Method Not Allowed"
    message = "Sorry, but the requested method is not supported."


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
