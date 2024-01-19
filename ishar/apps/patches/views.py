from django.views.generic import ListView

from ishar.apps.patches.models import Patch


class PatchesAllView(ListView):
    """
    Patches base list view of all patches.
    """
    context_object_name = "patches"
    model = Patch
    queryset = model.objects.filter(
        is_visible=True
    ).order_by(
        "-patch_date"
    ).all()
    template_name = "patches.html"


class PatchesLatestView(PatchesAllView):
    model = Patch
    queryset = model.objects.filter(
        is_visible=True
    ).order_by(
        "-patch_date"
    ).all()[:1]


class PatchesListView(PatchesAllView):
    paginate_by = 5
