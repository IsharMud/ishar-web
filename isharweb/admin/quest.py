from django.contrib.admin import ModelAdmin, TabularInline

from ..models.quest.step import QuestStep


class QuestStepAdmin(TabularInline):
    """
    Ishar quest step administration.
    """
    model = QuestStep
    fieldsets = (
        (None, {"fields": ["step_id", "step_type", "quest"]}),
        ("Details", {"fields": ["target", "num_required", "time_limit"]}),
        ("Mystify", {"fields": ["mystify", "mystify_text"]})
    )
    filter_horizontal = []
    filter_vertical = []
    list_display = ["step_id", "step_type", "quest"]
    list_filter = ["step_type", "num_required", "mystify", "quest"]
    ordering = ["step_id"]
    search_fields = ["step_id", "step_type", "target", "mystify_text"]
    readonly_fields = ["step_id"]


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
    inlines = [QuestStepAdmin]
    list_display = ["display_name", "_is_repeatable", "min_level", "max_level"]
    list_filter = ["repeatable", "min_level", "max_level"]
    ordering = ["quest_id"]
    search_fields = ["quest_id", "display_name", "name"]
    readonly_fields = ["quest_id"]
