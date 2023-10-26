from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe

from ishar.apps.quests.models import Quest, QuestPrereq, QuestReward, QuestStep


def get_quest_class_link(obj=None) -> (str, None):
    if obj and obj.get_class_restrict_display() is not None:
        return mark_safe(
            '<a href="%s">%s</a>' % (
                reverse(
                    viewname="admin:classes_class_change",
                    args=(obj.class_restrict,)
                ),
                obj.get_class_restrict_display()
            )
        )
    return None


def get_quest_name_link(obj=None) -> (str, None):
    if obj is not None:
        return mark_safe(
            '<a href="%s">%s</a>' % (
                reverse(
                    viewname="admin:quests_quest_change",
                    args=(obj.quest.quest_id,)
                ),
                obj.quest.display_name
            )
        )
    return None


@admin.register(QuestPrereq)
class QuestPrereqsAdmin(admin.ModelAdmin):
    """
    Ishar quest prerequisite administration.
    """
    fieldsets = (
        (None, {"fields": ("quest", "required_quest")}),
    )
    list_display = ("quest", "required_quest")
    list_filter = (
        ("quest", admin.RelatedOnlyFieldListFilter),
        ("required_quest", admin.RelatedOnlyFieldListFilter)
    )
    model = QuestPrereq
    search_fields = (
        "quest__name", "quest__display_name", "quest__class_restrict",
        "required_quest__name", "required_quest__display_name",
        "required_quest__class_restrict"
    )

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_change_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
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
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_change_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False


class QuestRewardsAdminInline(admin.TabularInline):
    """
    Ishar quest reward administration inline.
    """
    extra = 1
    model = QuestReward

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_change_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False


class QuestStepsAdminInline(admin.TabularInline):
    """
    Ishar quest step administration inline.
    """
    extra = 1
    model = QuestStep

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_change_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
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

    @admin.display(description="Class", ordering="class_restrict")
    def get_quest_class_link(self, obj=None) -> (str, None):
        if obj.get_class_restrict_display():
            return mark_safe(
                '<a href="%s">%s</a>' % (
                    reverse(
                        viewname="admin:classes_class_change",
                        args=(obj.class_restrict,)
                    ),
                    obj.get_class_restrict_display()
                )
            )
        return None

    @admin.display(description="# Steps", ordering="num_steps")
    def num_steps(self, obj):
        return obj.num_steps

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_change_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
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
        return get_quest_name_link(obj=obj)

    @admin.display(description="Class", ordering="class_restrict")
    def get_quest_class_link(self, obj=None):
        return get_quest_class_link(obj=obj)

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_change_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
