from django.conf import settings
from django.contrib.admin import SimpleListFilter


class ImmortalTypeListFilter(SimpleListFilter):
    """Find players of certain immortal type by "__common__level"."""
    title = "Immortal Type"
    parameter_name = "immortal_type"

    def lookups(self, request, model_admin):
        return settings.IMMORTAL_LEVELS

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(common__level=self.value())
        return queryset
