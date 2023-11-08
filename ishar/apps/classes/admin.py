from django.contrib import admin

from ishar.apps.classes.models import Class, ClassLevel, ClassRace, ClassSkill


class ClassLevelInlineAdmin(admin.TabularInline):
    """
    Class Levels tabular inline administration.
    """
    classes = ("collapse",)
    extra = 1
    fields = ("level", "male_title", "female_title", "experience")
    model = ClassLevel

    def has_add_permission(self, request, obj) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False


class ClassRaceInlineAdmin(admin.TabularInline):
    """
    Class Race tabular inline administration.
    """
    classes = ("collapse",)
    extra = 1
    fields = ("race", "player_class")
    model = ClassRace

    def has_add_permission(self, request, obj) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_view_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False


class ClassSkillInlineAdmin(admin.TabularInline):
    """
    Class Skill tabular inline administration.
    """
    classes = ("collapse",)
    extra = 1
    fields = ("player_class", "skill", "min_level", "max_learn")
    model = ClassSkill

    def has_add_permission(self, request, obj) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_delete_permission(self, request, obj) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_view_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False


@admin.register(Class)
class ClassesAdmin(admin.ModelAdmin):
    """
    Ishar class administration.
    """
    fieldsets = (
        (None, {"fields": (
            "class_id", "class_name", "class_display", "class_description",
            "is_playable"
        )}),
        ("Other", {"fields": ("attack_per_level", "spell_rate")}),
        ("Stat", {"fields": ("class_dc", "class_stat")}),
        ("Hit Points", {"fields": ("base_hit_pts", "hit_pts_per_level")}),
        ("Base", {"fields": (
            "base_fortitude", "base_resilience", "base_reflex"
        )}),
    )
    inlines = (
        ClassLevelInlineAdmin, ClassRaceInlineAdmin, ClassSkillInlineAdmin
    )
    list_filter = ("is_playable",)
    list_display = list_display_links = (
        "class_id", "get_class_name", "is_playable"
    )
    ordering = ("-is_playable",)
    readonly_fields = ("class_id",)
    search_fields = ("class_name", "class_display", "class_description")

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
