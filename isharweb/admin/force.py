from django.contrib.admin import ModelAdmin


class ForceAdmin(ModelAdmin):
    """
    Ishar force administration.
    """
    fieldsets = (
        (None, {"fields": ("force_name",)}),
    )
    filter_horizontal = ()
    filter_vertical = ()
    list_display = ["force_name"]
    list_filter = ()
    readonly_fields = ()
    search_fields = ["force_name"]
