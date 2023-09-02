from django.contrib import admin

from ..models.reward import QuestReward


@admin.register(QuestReward)
class QuestRewardAdmin(admin.ModelAdmin):
    """
    Ishar quest reward administration.
    """
    fieldsets = (
        ("Type", {"fields": ("reward_type",)}),
        ("Amount", {"fields": ("reward_num",)}),
        ("Quest", {"fields": ("quest",)}),
        ("Classes", {"fields": ("class_restrict",)})
    )
    filter_horizontal = filter_vertical = readonly_fields = ()
    list_display = ("reward_num", "reward_type", "quest", "class_restrict")
    list_filter = ("reward_type", "class_restrict", "quest")
    model = QuestReward
    search_fields = ("reward_num", "reward_type", "quest", "class_restrict")


class QuestRewardAdminInline(admin.TabularInline):
    """
    Ishar quest reward administration inline.
    """
    extra = 1
    # fields = ("reward_type", "reward_num", "quest", "class_restrict")
    model = QuestReward
