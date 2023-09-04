from django.views.generic import ListView

from .models import Patch


class PatchAllView(ListView):
    context_object_name = "patches"
    model = Patch
    template_name = "patches.html.djt"


class PatchListView(PatchAllView):
    paginate_by = 3
