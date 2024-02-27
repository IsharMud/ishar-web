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
        ordering = ("force_name",)
        verbose_name = "Force"

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return self.force_name
