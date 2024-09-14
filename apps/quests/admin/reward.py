from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from ..models.reward import QuestReward


@admin.register(QuestReward)
class QuestRewardAdmin(admin.ModelAdmin):
    """
    Quest reward administration.
    """
    fieldsets = (
        (None, {"fields": ("quest_reward_id",)}),
        ("Type", {"fields": ("reward_type",)}),
        ("Number", {"fields": ("reward_num",)}),
        ("Quest", {"fields": ("quest",)}),
        ("Class", {"fields": ("class_restrict",)})
    )
    list_display = (
        "quest_reward_id", "reward_type",
        "get_quest_name_link", "get_quest_class_link"
    )
    list_display_links = ("quest_reward_id", "reward_type")
    list_filter = (
        "reward_type", "class_restrict",
        ("quest", admin.RelatedOnlyFieldListFilter)
    )
    model = QuestReward
    readonly_fields = ("quest_reward_id",)
    search_fields = (
        "reward_num", "reward_type", "quest__display_name", "class_restrict"
    )

    @admin.display(description="Quest", ordering="quest__display_name")
    def get_quest_name_link(self, obj=None):
        if obj.quest and obj.quest.display_name:
            return format_html(
                '<a href="{}">{}</a>',
                reverse(
                    viewname="admin:quests_quest_change",
                    args=(obj.quest.quest_id,)
                ),
                obj.quest.display_name
            )
        return None

    @admin.display(description="Class", ordering="quest__class_restrict")
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
