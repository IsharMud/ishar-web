from django.views.generic import ListView

from apps.patches.models import Patch


class BasePatchView(ListView):
    """Patches base list view lists all patches."""
    context_object_name = "patches"
    model = Patch
    template_name = "patches.html"

    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True).all()


class PatchesLatestView(BasePatchView):
    """Latest patch view."""

    def get_queryset(self):
        # Return a list of the single most recent item
        return super().get_queryset().all()[:1]


class PatchesView(BasePatchView):
    """Paginated view of patches."""
    paginate_by = 5
