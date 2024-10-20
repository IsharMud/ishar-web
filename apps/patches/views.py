from django.views.generic import ListView

from apps.patches.models import Patch


class BasePatchView(ListView):
    """Patches base list view lists all patches."""

    context_object_name = "patches"
    model = Patch
    template_name = "patches.html"

    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True).all()


class PatchesView(BasePatchView):
    """Main paginated view of patches."""

    paginate_by = 5


class PatchesLatestView(BasePatchView):
    template_name = "latest.html"

    def get_queryset(self):
        return super().get_queryset().all()[:1]
