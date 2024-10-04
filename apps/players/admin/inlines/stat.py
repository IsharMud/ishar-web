from django.contrib.admin import display, StackedInline
from django.utils.timesince import timesince
from django.utils.timezone import now

from ...models.stat import PlayerStat


class PlayerStatInlineAdmin(StackedInline):
    """Player stat inline administration."""

    model = PlayerStat
    fieldsets = (
        ("Time", {"fields": ("get_total_play_time", "get_remort_play_time")}),
        ("Deaths", {"fields": ("total_deaths", "remort_deaths")}),
        ("Renown", {"fields": ("total_renown", "remort_renown")}),
        ("Challenges", {"fields": ("total_challenges", "remort_challenges")}),
        ("Quests", {"fields": ("total_quests", "remort_quests")}),
    )
    readonly_fields = ("get_remort_play_time", "get_total_play_time")
    verbose_name = verbose_name_plural = "Statistics"

    @display(description="Remort Play Time", ordering="remort_play_time")
    def get_remort_play_time(self, obj) -> str:
        """Human-readable player remort play time."""
        return timesince(now() - obj.get_remort_play_timedelta())

    @display(description="Total Play Time", ordering="total_play_time")
    def get_total_play_time(self, obj) -> str:
        """Human-readable player total play time."""
        return timesince(now() - obj.get_total_play_timedelta())

    def has_add_permission(self, request, obj) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
