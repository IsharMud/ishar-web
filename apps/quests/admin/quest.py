from django.contrib.admin import display, ModelAdmin, register
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from ..models.quest import Quest

from .inlines.prereq import QuestPrereqTabularInline
from .inlines.reward import QuestRewardTabularInline
from .inlines.step import QuestStepTabularInline


@register(Quest)
class QuestAdmin(ModelAdmin):
    """
    Quest administration.
    """

    fieldsets = (
        (None, {"fields": ("quest_id", "name", "display_name", "repeatable")}),
        ("Deprecated", {
            "fields": ("deprecated_max_level", "deprecated_prerequisite")
        }),
        ("Players", {"fields": ("min_level", "class_restrict",)}),
        ("Messages", {"fields": (
            "description", "quest_intro", "completion_message"
        )}),
        ("Mobiles", {"fields": ("quest_source", "quest_return")}),
        ("Items", {"fields": ("start_item",)}),
    )
    inlines = (
        QuestPrereqTabularInline,
        QuestStepTabularInline,
        QuestRewardTabularInline
    )
    list_display = (
        "quest_id", "display_name", "repeatable", "num_steps",
        "get_quest_class_link"
    )
    list_display_links = ("quest_id", "display_name")
    list_filter = ("repeatable", "class_restrict", "min_level")
    readonly_fields = (
        "quest_id", "deprecated_prerequisite", "deprecated_max_level"
    )
    search_fields = (
        "quest_id", "display_name", "name", "description",
        "completion_message", "quest_intro",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            num_steps=Count("step")
        )

    @display(description="Class", ordering="class_restrict")
    def get_quest_class_link(self, obj=None) -> (str, None):
        if obj.get_class_restrict_display():
            return format_html(
                '<a href="{}">{}</a>',
                reverse(
                    viewname="admin:classes_class_change",
                    args=(obj.class_restrict,)
                ),
                obj.get_class_restrict_display()
            )
        return None

    @display(description="# Steps", ordering="num_steps")
    def num_steps(self, obj):
        return obj.num_steps

    def save_model(self, request, obj, form, change):
        if obj and not change:
            obj.deprecated_prerequisite = '-1'
            obj.deprecated_max_level = '20'
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request) -> bool:
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)
