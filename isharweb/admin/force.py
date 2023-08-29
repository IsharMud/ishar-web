from django.contrib.admin import ModelAdmin


class ForceAdmin(ModelAdmin):
    """
    Ishar force administration.
    """
    fieldsets = ((None, {"fields": ("force_name",)}),)
    filter_horizontal = filter_vertical = list_filter = readonly_fields = ()
    list_display = search_fields = fieldsets[0][1]["fields"]
