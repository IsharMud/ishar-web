from django.contrib import admin
from django.db import models


class Class(models.Model):
    """
    Character/Mobile Class.
    """
    class_id = models.AutoField(
        primary_key=True,
        help_text=(
            "Auto-generated permanent identification number of the class."
        ),
        verbose_name="Class ID"
    )
    class_name = models.CharField(
        unique=True, max_length=15,
        help_text="Name of the class.",
        verbose_name="Class Name"
    )
    class_display = models.CharField(
        max_length=32, blank=True, null=True,
        help_text="Display phrase of the class.",
        verbose_name="Class Display"
    )
    class_description = models.CharField(
        max_length=64, blank=True, null=True,
        help_text=(
            "Description of the class. "
            "Blank indicates that the class is not playable."
        ),
        verbose_name="Class Description"
    )

    class Meta:
        managed = False
        db_table = "classes"
        default_related_name = "class"
        ordering = ("-class_description", "class_name",)
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} [{self.class_id}]"

    def __str__(self) -> str:
        return self.get_class_name()

    @admin.display(description="Class Name", ordering="class_name")
    def get_class_name(self) -> str:
        """Formatted class name."""
        return self.class_name.replace("_", " ").title()

    @admin.display(
        boolean=True, description="Playable?", ordering="class_description"
    )
    def is_playable(self) -> bool:
        """Boolean whether the class is playable."""
        if self.class_description:
            return True
        return False
