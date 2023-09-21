from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Quest, QuestPrereq, QuestReward, QuestStep


@admin.register(QuestPrereq)
class QuestPrereqsAdmin(admin.ModelAdmin):
    """
    Ishar quest prerequisite administration.
    """
    fieldsets = (
        (None, {"fields": ("quest", "required_quest")}),
    )
    list_display = search_fields = ("quest", "required_quest")
    list_filter = (("quest", admin.RelatedOnlyFieldListFilter),)
    model = QuestPrereq

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False


class QuestPrereqsAdminInline(admin.TabularInline):
    """
    Ishar quest prerequisite administration inline.
    """
    extra = 1
    fk_name = "quest"
    model = QuestPrereq

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False


class QuestRewardsAdminInline(admin.TabularInline):
    """
    Ishar quest reward administration inline.
    """
    extra = 1
    model = QuestReward

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False


class QuestStepsAdminInline(admin.TabularInline):
    """
    Ishar quest step administration inline.
    """
    extra = 1
    model = QuestStep

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False


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
    inlines = (
        QuestPrereqsAdminInline, QuestStepsAdminInline, QuestRewardsAdminInline
    )
    list_display = (
        "quest_id", "display_name", "repeatable", "class_restrict", "min_level"
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

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False

    def save_model(self, request, obj, form, change):
        if obj and not change:
            obj.deprecated_prerequisite = '-1'
            obj.deprecated_max_level = '20'
        super().save_model(request, obj, form, change)


@admin.register(QuestReward)
class QuestRewardsAdmin(admin.ModelAdmin):
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
    list_display = ("quest_reward_id", "reward_type", "quest", "class_restrict")
    list_filter = (
        "reward_type", "class_restrict",
        ("quest", admin.RelatedOnlyFieldListFilter)
    )
    model = QuestReward
    readonly_fields = ("quest_reward_id",)
    search_fields = ("reward_num", "reward_type", "quest", "class_restrict")

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False


@admin.register(QuestStep)
class QuestStepsAdmin(admin.ModelAdmin):
    """
    Ishar quest step administration.
    """

    @admin.display(description="Class")
    def get_quest_class(self, obj):
        return obj.quest.get_class_restrict_display()

    fieldsets = (
        (None, {"fields": ("step_id", "step_type", "quest")}),
        ("Details", {"fields": ("target", "num_required", "time_limit")}),
        ("Mystify", {"fields": ("mystify", "mystify_text")})
    )
    list_display = (
        "step_id", "step_type", "quest", "get_quest_class", "mystify"
    )
    list_display_links = ("step_id", "step_type")
    list_filter = (
        "step_type", "quest__class_restrict", "mystify",
        ("quest", admin.RelatedOnlyFieldListFilter), "num_required"
    )
    model = QuestStep
    readonly_fields = ("step_id", "get_quest_class")
    search_fields = (
        "step_id", "step_type", "target", "mystify_text",
        "quest__name", "quest__display_name", "quest__class_restrict"
    )

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False
