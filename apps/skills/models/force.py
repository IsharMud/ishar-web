from django.db import models


class ForceManager(models.Manager):
    def get_by_natural_key(self, force_name):
        """Natural key by force name."""
        return self.get(force_name=force_name)


class Force(models.Model):
    """Ishar force."""
    objects = ForceManager()

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

    def natural_key(self) -> str:
        """Natural key by force name."""
        return self.force_name
