from django.conf import settings
from django.views.generic.base import RedirectView, TemplateView

from ishar.apps.news.models import News


class ConnectRedirectView(RedirectView):
    permanent = True
    url = settings.CONNECT_URL


class PortalView(TemplateView):
    template_name = "portal.html.djt"


class SupportView(TemplateView):
    template_name = "support.html.djt"


class WelcomeView(TemplateView):
    template_name = "welcome.html.djt"
    extra_context = {"news": News.objects.all()}
