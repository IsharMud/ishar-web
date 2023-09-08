from django.contrib import admin

from .models import Challenge


@admin.register(Challenge)
class ChallengesAdmin(admin.ModelAdmin):
    """
    Ishar challenge administration.
    """
    fieldsets = (
        (None, {"fields": ("challenge_id", "is_active")}),
        ("Details", {"fields": ("challenge_desc", "winner_desc")}),
        ("Target", {"fields": ("mob_vnum", "mob_name")}),
        ("Original", {"fields": ("orig_level", "orig_people", "orig_tier")}),
        ("Adjusted", {"fields": ("adj_level", "adj_people", "adj_tier")}),
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("challenge_desc", "is_active", "_is_completed")
    list_filter = ("is_active",)
    readonly_fields = ("challenge_id",)
    search_fields = ("challenge_desc", "winner_desc", "mob_vnum", "mob_name")

    def has_add_permission(self, request, obj=None):
        return request.user.is_god()

    def has_change_permission(self, request, obj=None):
        return request.user.is_god()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_god()
