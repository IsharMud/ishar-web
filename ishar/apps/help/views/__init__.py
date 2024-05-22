from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from ..forms import HelpSearchForm
from ..utils.get import get_help_topics


HELP_PROPERTIES = (
    "syntax", "level", "minimum", "class", "component", "topic", "save", "stats"
)


class HelpView(TemplateView):
    """
    Help view.
    """
    template_name = "help_page.html"
    help_topics = get_help_topics()
    help_topic = None
    http_method_names = ("get", "post")
    search_form = HelpSearchForm()
    status = 200

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["help_properties"] = HELP_PROPERTIES
        context["help_search_form"] = self.search_form
        context["help_topic"] = self.help_topic
        context["help_topics"] = self.help_topics
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        return redirect(
            to="help_page",
            help_topic=request.POST.get("search_topic")
        )
