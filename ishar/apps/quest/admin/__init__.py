from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .reward import QuestRewardAdminInline
from .step import QuestStepAdminInline

from ..models import Quest


@admin.register(Quest)
class QuestAdmin(ModelAdmin):
    """
    Ishar quest administration.
    """

    fieldsets = (
        (None, {"fields": (
            "name", "display_name", "repeatable", "prerequisite"
        )}),
        ("Classes", {"fields": ("class_restrict",)}),
        ("Levels", {"fields": ("min_level", "max_level")}),
        ("Messages", {"fields": (
            "description", "quest_intro", "completion_message"
        )}),
        ("Mobiles", {"fields": ("quest_source", "quest_return")})
    )
    filter_horizontal = filter_vertical = ()
    inlines = (QuestStepAdminInline, QuestRewardAdminInline)
    list_display = (
        "display_name", "repeatable", "class_restrict",
        "for_levels", "step_count"
    )
    list_filter = ("repeatable", "class_restrict", "min_level", "max_level")
    readonly_fields = ("quest_id", "prerequisite")
    search_fields = (
        "quest_id", "display_name", "name", "description",
        "completion_message", "quest_intro",
    )
