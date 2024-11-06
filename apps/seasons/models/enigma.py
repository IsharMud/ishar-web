from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.textarea import NoStripTextareaField


class SeasonalEnigma(models.Model):
    """Ishar Seasonal Enigma."""

    seasonal_enigma_id = models.AutoField(
        primary_key=True,
        help_text=_(
            "Auto-generated primary key ID number of the seasonal enigma."
        ),
        verbose_name=_("Seasonal Enigma ID")
    )
    enigma_name = NoStripTextareaField(
        blank=True,
        max_length=100,
        null=True,
        help_text=_("Name of the seasonal enigma."),
        verbose_name=_("Enigma Name")
    )
    enigma_welcome = NoStripTextareaField(
        blank=True,
        max_length=216,
        null=True,
        help_text=_("Welcome message of the seasonal enigma."),
        verbose_name=_("Enigma Welcome")
    )
    enigma_intro_connect = NoStripTextareaField(
        blank=True,
        max_length=2056,
        null=True,
        help_text=_("Introduction connection message of the seasonal enigma."),
        verbose_name=_("Enigma Intro Connect")
    )
    enigma_character_select = NoStripTextareaField(
        blank=True,
        max_length=2056,
        null=True,
        help_text=_("Character select message of the seasonal enigma."),
        verbose_name=_("Enigma Character Select")
    )

    class Meta:
        managed = False
        db_table = "seasonal_enigma"
        default_related_name = "seasonal_enigma"
        get_latest_by = ordering = ("-seasonal_enigma_id",)
        verbose_name = "Seasonal Enigma"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.enigma_name}"