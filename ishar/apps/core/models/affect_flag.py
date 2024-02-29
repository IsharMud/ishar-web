from django.db import models


class AffectFlag(models.Model):
    """Ishar affect flag, used by both mobiles and players."""
    flag_id = models.PositiveIntegerField(
        blank=False,
        help_text="Auto-generated identification number of the affect flag.",
        null=False,
        primary_key=True,
        verbose_name="Affect Flag ID"
    )
    name = models.CharField(
        unique=True,
        max_length=30,
        help_text="(Internal) name of the affect flag.",
        verbose_name="Name"
    )
    display_name = models.CharField(
        max_length=100,
        help_text="Display name of the affect flag.",
        verbose_name="Display Name"
    )
    is_beneficial = models.IntegerField(
        blank=True,
        null=True,
        help_text="Is the affect flag beneficial?",
        verbose_name="Beneficial?"
    )
    item_description = models.CharField(
        max_length=100,
        help_text="Item description of the affect flag.",
        verbose_name="Item Description"
    )

    class Meta:
        managed = False
        db_table = "affect_flags"
        default_related_name = "affect_flag"
        ordering = ("display_name",)
        verbose_name = "Affect Flag"
        verbose_name_plural = "Affect Flags"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return self.display_name
