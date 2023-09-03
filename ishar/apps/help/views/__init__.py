from django.views.generic.base import TemplateView


class HelpView(TemplateView):
    template_name = "help_page.html.djt"


class HelpPageView(TemplateView):
    template_name = "help_page.html.djt"


class BackgroundView(TemplateView):
    template_name = "history.html.djt"


class HistoryView(BackgroundView):
    pass


class StartView(TemplateView):
    template_name = "start.html.djt"
