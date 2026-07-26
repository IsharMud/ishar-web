from django.db import models
from django.utils.translation import gettext_lazy as _


class Enchantment(models.Model):
    """Ishar enchantment definition ("enchantments" game table)."""

    id = models.AutoField(
        primary_key=True,
        help_text=_("Primary key identification number of the enchantment."),
        verbose_name=_("Enchantment ID"),
    )
    enum_symbol = models.CharField(
        max_length=64,
        unique=True,
        help_text=_("Game code enumeration symbol of the enchantment."),
        verbose_name=_("Enum Symbol"),
    )
    name = models.CharField(
        max_length=128,
        help_text=_("Name of the enchantment."),
        verbose_name=_("Name"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Description of the enchantment."),
        verbose_name=_("Description"),
    )
    obj_display = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        help_text=_("String displayed on objects carrying the enchantment."),
        verbose_name=_("Object Display"),
    )
    gear_type = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("Target gear type of the enchantment."),
        verbose_name=_("Gear Type"),
    )
    is_exotic = models.BooleanField(
        default=False,
        help_text=_(
            "Has special combat handling beyond stat modifiers."
        ),
        verbose_name=_("Is Exotic?"),
    )

    class Meta:
        managed = False
        db_table = "enchantments"
        default_related_name = "enchantment"
        ordering = ("name",)
        verbose_name = _("Enchantment")
        verbose_name_plural = _("Enchantments")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.name
