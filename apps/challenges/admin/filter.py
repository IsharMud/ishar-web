from django.contrib.admin import SimpleListFilter


class ChallengeCompletedListFilter(SimpleListFilter):
    """Admin list filter to identify (in)complete challenges."""
    title = "Completed"
    parameter_name = "is_completed"

    def lookups(self, request, model_admin):
        return (
            (1, "Yes"),
            (0, "No")
        )

    def queryset(self, request, queryset):
        """
        Determine whether a challenge is complete based on whether
            the "winner_desc" column is empty or not.
        """
        qs = queryset
        if self.value():
            if self.value() == "1":
                return qs.exclude(winner_desc__exact="")
            if self.value() == "0":
                return qs.filter(winner_desc__exact="")
        return qs
