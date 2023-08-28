from django.db import models


class Force(models.Model):
    """
    Force.
    """
    force_name = models.CharField(
        unique=True,
        max_length=255,
        blank=True,
        null=True,
        help_text="Name of the force.",
        verbose_name="Force Name"
    )

    class Meta:
        managed = False
        db_table = "forces"
        ordering = ["force_name"]
        verbose_name = "Force"
        verbose_name_plural = "Forces"

    def __repr__(self):
        return f"Force: {repr(self.__str__())}"

    def __str__(self):
        return self.force_name
