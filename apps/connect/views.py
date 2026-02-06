from django.views.generic.base import TemplateView


class ConnectView(TemplateView):
    """MUD web client connection page."""

    template_name = "connect.html"
