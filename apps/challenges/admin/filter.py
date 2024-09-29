from django.contrib.admin import SimpleListFilter


class ChallengeCompletedListFilter(SimpleListFilter):
    """Admin list filter to identify (in)complete challenges."""
    title = "Completed?"
    parameter_name = "completed"

    def lookups(self, request, model_admin):
        return (
            ("1", "Yes"),
            ("0", "No")
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == "1":
                queryset = queryset.exclude(winner_desc__exact="")
            if self.value() == "0":
                queryset = queryset.filter(winner_desc__exact="")
        return queryset
