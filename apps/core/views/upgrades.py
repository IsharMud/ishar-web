from django.views.generic.base import TemplateView

from apps.players.models.remort_upgrade import RemortUpgrade


class UpgradesView(TemplateView):
    """Information about player remort upgrades, and their cost."""
    template_name = "upgrades.html"

    def get_context_data(self, **kwargs):
        # Include sorted active/enabled available player remort upgrades.
        context = super().get_context_data(**kwargs)
        context["upgrades"] = RemortUpgrade.objects.filter(
            can_buy__exact=True
        ).order_by("name").all()
        return context
