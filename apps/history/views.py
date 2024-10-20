from django.views.generic.base import TemplateView


class HistoryView(TemplateView):
    """History page."""

    template_name = "history.html"
