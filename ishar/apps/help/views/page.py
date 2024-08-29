from django.contrib import messages
from django.shortcuts import redirect, reverse
from logging import getLogger

from ..views import HelpView


logger = getLogger(__name__)

class HelpPageView(HelpView):
    """
    Help page view.
    """
    template_name = "help_page.html"

    def dispatch(self, request, *args, **kwargs):

        # Get help topic name from URL.
        help_topic = kwargs.get("help_topic")
        if help_topic is not None:

            # Match exact topic names for display.
            if help_topic in self.help_topics:
                self.help_topic = self.help_topics[help_topic]
                return super().dispatch(request, *args, **kwargs)

            # Otherwise, try a variety of formats of the URL topic name.
            for fmt in (
                help_topic, help_topic.strip(), help_topic.title(),
                help_topic.lower(), help_topic.upper()
            ):

                # Redirect to actual help topic name, if necessary.
                topic = self.help_topics.get(fmt)
                if topic:
                    return redirect(
                        to=reverse(viewname="help_page", args=(topic.name,))
                    )

            self.status = 404
            messages.error(
                request=request,
                message="Sorry, but no such help topic could be found."
            )

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Set HTTP response status code.
        """
        return self.render_to_response(
            context=self.get_context_data(**kwargs),
            status=self.status
        )
