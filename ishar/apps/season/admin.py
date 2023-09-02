from django.contrib import admin

from .models import Season


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    """
    Ishar season administration.
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
    filter_horizontal = filter_vertical = ()
    list_display = (
        "season_id", "is_active", "effective_date", "expiration_date"
    )
    list_filter = ("is_active",)
    readonly_fields = ("season_id",)
    search_fields = (
        "seasonal_leader_name", "effective_date", "expiration_date"
    )
