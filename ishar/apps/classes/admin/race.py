from django.contrib.admin import ModelAdmin, register

from ishar.apps.classes.models.race import ClassRace


@register(ClassRace)
class ClassRaceAdmin(ModelAdmin):
    """
    Ishar class race administration.
    """
    list_display = ("classes_races_id", "player_class", "race")
    list_display_links = list_display
    list_filter = ("player_class", "race")
