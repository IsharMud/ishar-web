from django.contrib.admin import ModelAdmin


class ClassLevelAdmin(ModelAdmin):
    """Ishar class level administration."""

    list_display = ("class_level_id", "player_class", "level")
    list_display_links = list_display
    list_filter = ("player_class", "level")
