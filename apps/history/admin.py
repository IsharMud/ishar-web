from django.contrib import admin

from .models import HistoricSeasonStat


@admin.register(HistoricSeasonStat)
class HistoryAdmin(admin.ModelAdmin):
    """Historic administration."""

    fields = readonly_fields = (
        "season", "account", "player_name", "remorts", "player_class", "race",
        "total_renown", "challenges_completed", "quests_completed", "deaths",
        "game_type", "display_total_play_time", "level"
    )
    list_display = (
        "season", "account", "player_name", "remorts",
        "total_renown", "challenges_completed", "quests_completed", "deaths",
        "display_total_play_time"
    )
    list_display_links = ("season", "account", "player_name")
    list_filter = (
        ("season", admin.RelatedOnlyFieldListFilter),
        ("account", admin.RelatedOnlyFieldListFilter),
        ("player_class", admin.RelatedOnlyFieldListFilter),
        ("race", admin.RelatedOnlyFieldListFilter),
        "game_type"
    )
    search_fields = ("account__account_name", "player_name")
    show_facets = admin.ShowFacets.ALWAYS
    show_full_result_count = True

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj=obj)

    @admin.display(description="Play Time", ordering="play_time")
    def display_total_play_time(self, obj=None):
        return obj.display_total_play_time()
