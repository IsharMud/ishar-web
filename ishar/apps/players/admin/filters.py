from django.conf import settings
from django.contrib.admin import SimpleListFilter


class ImmortalTypeListFilter(SimpleListFilter):
    """
    Determine whether a player is certain type of immortal,
        based on their "true_level" column value.
    """
    title = "Immortal Type"
    parameter_name = "immortal_type"

    def lookups(self, request, model_admin):
        return settings.IMMORTAL_LEVELS

    def queryset(self, request, queryset):
        qs = queryset
        if self.value():
            qs = qs.filter(common__level=self.value())
        return qs
