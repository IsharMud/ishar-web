from django.contrib.admin import display, ModelAdmin, register

from ..models.season import Season


@register(Season)
class SeasonAdmin(ModelAdmin):
    """Season administration."""

    date_hierarchy = "effective_date"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "season_id",
                    "is_active",
                    "game_state",
                )
            }
        ),
        (
            "Dates",
            {
                "fields": (
                    "effective_date",
                    "expiration_date",
                    "last_challenge_cycle",
                    "next_cycle",
                )
            },
        ),
        (
            "Multi-Play", {
                "fields": (
                    "multiplay_limit",
                )
            }
        ),
        (
            "Averages",
            {
                "fields": (
                    "average_essence_gain",
                    "average_remorts",
                    "avg_renown"
                )
            },
        ),
        (
            "Maximums",
            {
                "fields": (
                    "max_essence_gain",
                    "max_remorts",
                    "max_renown",
                    "total_remorts",
                )
            },
        ),
        (
            "Leader",
            {
                "fields": (
                    "season_leader_account",
                    "seasonal_leader_name",
                )
            }
        ),
    )
    list_display = list_display_links = (
        "season_id",
        "is_active",
        "effective_date",
        "expiration_date",
    )
    list_filter = (
        "is_active",
        "multiplay_limit"
    )
    readonly_fields = (
        "season_id",
        "next_cycle"
    )
    search_fields = (
        "seasonal_leader_name",
        "effective_date",
        "expiration_date",
    )

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    @display(
        description="Next Challenge Cycle",
        ordering="last_challenge_cycle"
    )
    def next_cycle(self, obj=None):
        return obj.get_next_cycle().strftime("%a, %b %d, %Y @ %I:%M:%S %p")
