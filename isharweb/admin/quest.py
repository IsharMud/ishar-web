from django.contrib.admin import ModelAdmin


class QuestAdmin(ModelAdmin):
    """
    Ishar quest administration.
    """

    fieldsets = (
        (None, {
            "fields": ["name", "display_name", "repeatable", "prerequisite"]
        }),
        ("Classes", {"fields": ["class_restrict"]}),
        ("Levels", {"fields": ["min_level", "max_level"]}),
        ("Messages", {
            "fields": ["description", "quest_intro", "completion_message"]
        }),
        ("Mobiles", {"fields": ["quest_source", "quest_return"]})
    )
    filter_horizontal = []
    filter_vertical = []
    list_display = ["display_name", "_is_repeatable", "min_level", "max_level"]
    list_filter = ["min_level", "max_level", "repeatable"]
    ordering = ["quest_id"]
    search_fields = ["display_name", "name"]
    readonly_fields = []
