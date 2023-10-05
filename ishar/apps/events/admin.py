from django.contrib import admin

from ishar.apps.events.models import GlobalEvent


@admin.register(GlobalEvent)
class GlobalEventsAdmin(admin.ModelAdmin):
    """
    Ishar global event administration.
    """
    date_hierarchy = "end_time"
    fieldsets = (
        (None, {"fields": ("event_type", "event_name", "event_desc")}),
        ("Date/Time", {"fields": ("start_time", "end_time")}),
        ("Bonus", {"fields": ("xp_bonus", "shop_bonus", "celestial_luck")})
    )
    list_display = (
        "event_name", "event_desc", "start_time", "end_time", "celestial_luck"
    )
    list_display_links = ("event_name", "event_desc")
    list_filter = ("xp_bonus", "shop_bonus", "celestial_luck")
    ordering = ("-end_time",)
    readonly_fields = ("event_type",)
    search_fields = ("event_name", "event_desc", "start_time", "end_time")

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

