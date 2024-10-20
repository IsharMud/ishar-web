from django.views.generic.list import ListView

from apps.players.models.remort_upgrade import RemortUpgrade


class UpgradesView(ListView):
    """Information about enabled remort upgrades, and their costs."""

    context_object_name = "upgrades"
    model = RemortUpgrade
    queryset = model.objects.filter(can_buy__exact=True)
    template_name = "upgrades.html"
