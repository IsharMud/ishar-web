from django.contrib import admin

from .models import GlobalEvent


@admin.register(GlobalEvent)
class GlobalEventsAdmin(admin.ModelAdmin):
    """
    Ishar global event administration.
    """

    def has_add_permission(self, request, obj=None):
        """
        Disabling adding events in /admin/.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Disabling changing events in /admin/.
        """
        return False

    date_hierarchy = "end_time"
    fieldsets = (
        (None, {"fields": ("event_type", "event_name", "event_desc")}),
        ("Date/Time", {"fields": ("start_time", "end_time")}),
        ("Bonus", {"fields": ("xp_bonus", "shop_bonus", "celestial_luck")})
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("event_name", "event_desc", "start_time", "end_time")
    list_filter = ("xp_bonus", "shop_bonus", "celestial_luck")
    ordering = ("-end_time",)
    readonly_fields = ("event_type",)
    search_fields = ("event_name", "event_desc", "start_time", "end_time")
