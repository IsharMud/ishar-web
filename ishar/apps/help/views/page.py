from django.contrib import messages
from django.shortcuts import redirect

from ..util import search_help_topics
from ..views import HelpView


class HelpPageView(HelpView):
    """
    Help page view.
    """
    template_name = "help_page.html"

    def dispatch(self, request, *args, **kwargs):

        # Get help topic name from URL.
        help_topic = kwargs.get("help_topic")
        if help_topic is not None:
            if help_topic in self.help_topics:
                self.help_topic = self.help_topics[help_topic]
                return super().dispatch(request, *args, **kwargs)

            search_topics = search_help_topics(self.help_topics, help_topic)
            if not search_topics:
                messages.error(
                    request=request,
                    message="Sorry, but no such help topic was found."
                )
                self.status = 404

            if search_topics:
                if len(search_topics) == 1:
                    found_topic = next(iter(search_topics.values()))
                    return redirect(
                        to="help_page", help_topic=found_topic["name"]
                    )
                self.help_topics = search_topics

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Set HTTP response status code.
        """
        return self.render_to_response(
            context=self.get_context_data(**kwargs),
            status=self.status
        )
