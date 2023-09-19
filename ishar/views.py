"""
isharmud.com base views.
"""
from django.conf import settings
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
        context["news"] = News.objects.first()
        return context
