from django.contrib import admin

from ..models.prereq import QuestPrereq


@admin.register(QuestPrereq)
class QuestPrereqsAdmin(admin.ModelAdmin):
    """
    Ishar quest prerequisite administration.
    """
    fieldsets = (
        (None, {"fields": ("quest", "required_quest")}),
    )
    filter_horizontal = filter_vertical = ()
    list_display = search_fields = ("quest", "required_quest")
    list_filter = (("quest", admin.RelatedOnlyFieldListFilter),)
    model = QuestPrereq

    def has_add_permission(self, request, obj=None):
        return request.user.is_immortal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_immortal()

    def has_view_or_change_permission(self, request, obj=None):
        return request.user.is_immortal()


class QuestPrereqsAdminInline(admin.TabularInline):
    """
    Ishar quest prerequisite administration inline.
    """
    fk_name = "quest"
    model = QuestPrereq

    def has_add_permission(self, request, obj=None):
        return request.user.is_immortal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_immortal()

    def has_view_or_change_permission(self, request, obj=None):
        return request.user.is_immortal()
