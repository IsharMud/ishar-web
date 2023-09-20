"""
isharmud.com base views.
"""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import RedirectView, TemplateView

from ishar.apps.news.models import News


class ClientsView(TemplateView):
    template_name = "clients.html.djt"


class ConnectRedirectView(RedirectView):
    permanent = True
    url = settings.CONNECT_URL


class FAQView(TemplateView):
    template_name = "faq.html.djt"


class HistoryView(TemplateView):
    template_name = "history.html.djt"


class IsharLoginView(LoginView):
    template_name = "login.html.djt"


class IsharLogoutView(LogoutView):
    template_name = "welcome.html.djt"

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have logged out!")
        return super().dispatch(request, *args, **kwargs)


class PortalView(TemplateView):
    template_name = "portal.html.djt"


class StartView(TemplateView):
    template_name = "start.html.djt"


class SupportView(TemplateView):
    template_name = "support.html.djt"


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
