from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .prereq import QuestPrereqAdminInline
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
            "name", "display_name", "repeatable", "deprecated_prerequisite"
        )}),
        ("Classes", {"fields": ("class_restrict",)}),
        ("Levels", {"fields": ("min_level", "deprecated_max_level")}),
        ("Messages", {"fields": (
            "description", "quest_intro", "completion_message"
        )}),
        ("Mobiles", {"fields": ("quest_source", "quest_return")})
    )
    filter_horizontal = filter_vertical = ()
    inlines = (
        QuestPrereqAdminInline, QuestStepAdminInline, QuestRewardAdminInline
    )
    list_display = ("display_name", "repeatable", "class_restrict", "min_level")
    list_filter = ("repeatable", "class_restrict", "min_level")
    readonly_fields = (
        "quest_id", "deprecated_prerequisite", "deprecated_max_level"
    )
    search_fields = (
        "quest_id", "display_name", "name", "description",
        "completion_message", "quest_intro",
    )

    def save_model(self, request, obj, form, change):
        if obj and not change:
            obj.deprecated_prerequisite = '-1'
            obj.deprecated_max_level = '20'
        super().save_model(request, obj, form, change)
