from django.contrib import admin

from ..models.reward import QuestReward


@admin.register(QuestReward)
class QuestRewardAdmin(admin.ModelAdmin):
    """
    Ishar quest reward administration.
    """
    fieldsets = (
        (None, {"fields": ("quest_reward_id",)}),
        ("Type", {"fields": ("reward_type",)}),
        ("Number", {"fields": ("reward_num",)}),
        ("Quest", {"fields": ("quest",)}),
        ("Class", {"fields": ("class_restrict",)})
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("quest_reward_id", "reward_type", "quest", "class_restrict")
    list_filter = (
        "reward_type", "class_restrict",
        ("quest", admin.RelatedOnlyFieldListFilter)
    )
    model = QuestReward
    readonly_fields = ("quest_reward_id",)
    search_fields = ("reward_num", "reward_type", "quest", "class_restrict")


class QuestRewardAdminInline(admin.TabularInline):
    """
    Ishar quest reward administration inline.
    """
    extra = 1
    # fields = ("reward_type", "reward_num", "quest", "class_restrict")
    model = QuestReward
