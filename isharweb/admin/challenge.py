from django.contrib.admin import ModelAdmin


class ChallengeAdmin(ModelAdmin):
    """
    Ishar challenge administration.
    """
    fieldsets = (
        (None, {"fields": ("challenge_id",)}),
        ("Details", {"fields": ("challenge_desc", "winner_desc")}),
        ("Target", {"fields": ("mob_vnum", "mob_name")}),
        ("Original", {"fields": ("orig_level", "orig_people", "orig_tier")}),
        ("Adjusted", {"fields": ("adj_level", "adj_people", "adj_tier")}),
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("challenge_desc", "_is_active", "_is_completed")
    list_filter = ("is_active",)
    readonly_fields = ("challenge_id",)
    search_fields = ("challenge_desc", "winner_desc", "mob_vnum", "mob_name")
