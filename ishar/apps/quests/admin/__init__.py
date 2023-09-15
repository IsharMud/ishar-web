from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .prereq import QuestPrereqsAdminInline
from .reward import QuestRewardsAdminInline
from .step import QuestStepsAdminInline

from ..models import Quest


@admin.register(Quest)
class QuestsAdmin(ModelAdmin):
    """
    Ishar quest administration.
    """

    fieldsets = (
        (None, {"fields": ("quest_id", "name", "display_name", "repeatable")}),
        ("Deprecated", {
            "classes": ("collapse",),
            "fields": ("deprecated_max_level", "deprecated_prerequisite")
        }),
        ("Players", {"fields": ("min_level", "class_restrict",)}),
        ("Messages", {"fields": (
            "description", "quest_intro", "completion_message"
        )}),
        ("Mobiles", {"fields": ("quest_source", "quest_return")})
    )
    filter_horizontal = filter_vertical = ()
    inlines = (
        QuestPrereqsAdminInline, QuestStepsAdminInline, QuestRewardsAdminInline
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

    def has_module_permission(self, request, obj=None):
        return request.user.is_immortal()

    def save_model(self, request, obj, form, change):
        if obj and not change:
            obj.deprecated_prerequisite = '-1'
            obj.deprecated_max_level = '20'
        super().save_model(request, obj, form, change)
