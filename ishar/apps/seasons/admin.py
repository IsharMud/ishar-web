from django.contrib import admin

from ishar.apps.seasons.models import Season


@admin.register(Season)
class SeasonsAdmin(admin.ModelAdmin):
    """
    Ishar seasons administration.
    """
    date_hierarchy = "effective_date"
    fieldsets = (
        (None, {"fields": ("season_id", "is_active")}),
        ("Dates", {"fields": (
            "effective_date", "expiration_date", "last_challenge_cycle"
        )}),
        ("Averages", {"fields": (
            "average_essence_gain", "average_remorts", "avg_renown"
        )}),
        ("Averages", {"fields": (
            "max_essence_gain", "max_remorts", "max_renown"
        )}),
        ("Leader", {"fields": (
            "season_leader_account", "seasonal_leader_name"
        )})
    )
    list_display = list_display_links = (
        "season_id", "is_active", "effective_date", "expiration_date"
    )
    list_filter = ("is_active",)
    readonly_fields = ("season_id",)
    search_fields = (
        "seasonal_leader_name", "effective_date", "expiration_date"
    )

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request):
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_change_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_view_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
