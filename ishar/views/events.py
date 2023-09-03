from django.views.generic.base import TemplateView


class EventsView(TemplateView):
    template_name = "events.html.djt"
