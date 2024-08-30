from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from ..forms import HelpSearchForm
from ..utils.helptab import HelpTab


class HelpView(TemplateView):
    """Help view."""
    template_name = "help_page.html"
    helptab = HelpTab()
    help_topic = None
    help_topics = {}
    http_method_names = ("get", "post")
    search_form = HelpSearchForm()
    status = 200

    def setup(self, request, *args, **kwargs):
        # Gather help topics from "helptab" file.
        self.help_topics = self.helptab.help_topics
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Include form, all help topics, and any specific help topic chosen.
        context = super().get_context_data(**kwargs)
        context["help_search_form"] = self.search_form
        context["help_topics"] = self.help_topics
        context["help_topic"] = self.help_topic
        return context

    def post(self, request, *args, **kwargs):
        # Redirect POST requests to HTTP GET search for the help topic string.
        return redirect(
            to="help_page",
            help_topic=request.POST.get("search_topic")
        )
