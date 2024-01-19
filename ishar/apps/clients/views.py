from django.views.generic.list import ListView

from ishar.apps.clients.models import MUDClientCategory  # , MUDClient


class MUDClientsView(ListView):
    """
    MUD Clients view.
    """
    context_object_name = "mud_client_categories"
    model = MUDClientCategory
    template_name = "clients.html"

    def get_queryset(self):
        return super().get_queryset().filter(is_visible__exact=1)
