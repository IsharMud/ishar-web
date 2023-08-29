from django.contrib.admin import ModelAdmin, TabularInline

from ..models.quest.reward import QuestReward
from ..models.quest.step import QuestStep


class QuestRewardAdminInline(TabularInline):
    """
    Ishar quest reward administration.
    """
    extra = 1
    fieldsets = (
        (None, {"fields": ("reward_num",)}),
        ("Type", {"fields": ("reward_type",)}),
        ("Quest", {"fields": ("quest",)}),
        ("Classes", {"fields": ("class_restrict",)})
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("reward_num", "reward_type", "quest", "class_restrict")
    list_filter = ("reward_type", "class_restrict", "quest")
    model = QuestReward
    search_fields = ("quest", "reward_type")
    readonly_fields = ()


class QuestStepAdminInline(TabularInline):
    """
    Ishar quest step administration inline.
    """
    extra = 1
    fieldsets = (
        (None, {"fields": ("step_id", "step_type", "quest")}),
        ("Details", {"fields": ("target", "num_required", "time_limit")}),
        ("Mystify", {"fields": ("mystify", "mystify_text")})
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("step_id", "step_type", "quest")
    list_filter = ("step_type", "num_required", "mystify", "quest")
    model = QuestStep
    search_fields = ("step_id", "step_type", "target", "mystify_text")
    readonly_fields = ("step_id",)


class QuestStepAdmin(ModelAdmin):
    """
    Ishar quest step administration inline.
    """
    fieldsets = (
        (None, {"fields": ("step_id", "step_type", "quest")}),
        ("Details", {"fields": ("target", "num_required", "time_limit")}),
        ("Mystify", {"fields": ("mystify", "mystify_text")})
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("step_id", "step_type", "quest")
    list_filter = ("step_type", "num_required", "mystify", "quest")
    model = QuestStep
    readonly_fields = ("step_id",)
    search_fields = ("step_id", "step_type", "target", "mystify_text")


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
    inlines = (QuestRewardAdminInline, QuestStepAdminInline)
    list_display = ("display_name", "_is_repeatable", "min_level", "max_level")
    list_filter = ("repeatable", "min_level", "max_level")
    readonly_fields = ("quest_id",)
    search_fields = (
        "quest_id", "display_name", "name", "description", "completion_message",
        "quest_intro",
    )
