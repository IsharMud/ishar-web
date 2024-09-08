from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.core.serializers import serialize
from django.views.generic.list import ListView

from apps.players.models.remort_upgrade import RemortUpgrade


class UpgradesView(LoginRequiredMixin, ListView, PermissionRequiredMixin):
    """Information about remort upgrades, and their costs."""
    context_object_name = "upgrades"
    model = RemortUpgrade
    permission_required = "remort_upgrade.view_remort_upgrade"
    queryset = model.objects.filter(can_buy__exact=True)
    template_name = "upgrades.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        json_object_name = f"{self.context_object_name}_json"
        context[json_object_name] = serialize(
            format="json",
            queryset=context.get(self.context_object_name).exclude(
#                max_value__exact=1
            ),
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True,
            fields=(
                "anchor", "display_name", "renown_cost", "tiers",
                "survival_renown_cost", "survival_tiers", "max_value",
            )
        )
        context[self.context_object_name] = context.get(
            self.context_object_name
        ).filter(
#            max_value__exact=1
        )
        return context
