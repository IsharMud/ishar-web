from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from ..forms import HelpSearchForm
from ..utils.helptab import HelpTab


HELP_PROPERTIES = (
    "syntax", "level", "minimum", "class", "component", "topic", "save", "stats"
)


helptab = HelpTab()

class HelpView(TemplateView):
    """
    Help view.
    """
    template_name = "help_page.html"
    helptab = HelpTab()
    help_topic = None
    help_topics = {}
    http_method_names = ("get", "post")
    search_form = HelpSearchForm()
    status = 200

    def setup(self, request, *args, **kwargs):
        self.help_topics = self.helptab.help_topics
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["help_search_form"] = self.search_form
        context["help_topic"] = self.help_topic
        context["help_topics"] = self.help_topics
        return context
