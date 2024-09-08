from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.views.generic.list import ListView

from apps.players.models.remort_upgrade import RemortUpgrade


class UpgradesView(LoginRequiredMixin, ListView, PermissionRequiredMixin):
    """Information about enabled remort upgrades, and their costs."""
    context_object_name = "upgrades"
    model = RemortUpgrade
    permission_required = "remort_upgrade.view_remort_upgrade"
    queryset = model.objects.filter(can_buy__exact=True)
    template_name = "upgrades.html"
