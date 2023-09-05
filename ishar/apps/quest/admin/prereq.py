from django.contrib import admin

from ..models.prereq import QuestPrereq


@admin.register(QuestPrereq)
class QuestPrereqAdmin(admin.ModelAdmin):
    """
    Ishar quest prerequisite administration.
    """
    fieldsets = (
        (None, {"fields": ("quest", "required_quest")}),
    )
    filter_horizontal = filter_vertical = ()
    list_display = search_fields = ("quest", "required_quest")
    list_filter = readonly_fields = (
        ("quest", admin.RelatedOnlyFieldListFilter),
    )
    model = QuestPrereq


class QuestPrereqAdminInline(admin.TabularInline):
    """
    Ishar quest prerequisite administration inline.
    """
    extra = 1
    fk_name = "quest"
    # fields = ("required_quest")
    model = QuestPrereq
