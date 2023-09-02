from django.contrib import admin
from django.db import models


class PlayerClass(models.Model):
    """
    Player Class.
    """
    class_id = models.AutoField(
        primary_key=True,
        help_text=(
            "Auto-generated permanent identification number "
            "of the player class."
        ),
        verbose_name="Class ID"
    )
    class_name = models.CharField(
        unique=True, max_length=15,
        help_text="Name of the player class.",
        verbose_name="Class Name"
    )
    class_display = models.CharField(
        max_length=32, blank=True, null=True,
        help_text="Display phrase of the player class.",
        verbose_name="Class Display"
    )
    class_description = models.CharField(
        max_length=64, blank=True, null=True,
        help_text="Description of the player class.",
        verbose_name="Class Description"
    )

    class Meta:
        managed = False
        db_table = "classes"
        default_related_name = "class"
        ordering = ("class_name",)
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __repr__(self) -> str:
        return f'Class: "{self.__str__()}" ({self.class_id})'

    def __str__(self) -> str:
        return self.class_name

    @admin.display(
        boolean=True, description="Playable", ordering="class_display"
    )
    def is_playable(self) -> bool:
        """
        Boolean whether the class is playable.
        """
        if self.class_display and self.class_description:
            return True
        return False

