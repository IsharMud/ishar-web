from django.db import models
from django.utils.translation import gettext_lazy as _


class Title(models.Model):
    """Ishar title."""

    title_id = models.AutoField(
        primary_key=True,
        help_text=_("Primary key identification number of the title."),
        verbose_name=_("Title ID")
    )
    male_text = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        help_text=_("Male text of the title."),
        verbose_name=_("Male Text")
    )
    female_text = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        help_text=_("Female text of the title."),
        verbose_name=_("Female Text")
    )
    prepend = models.BooleanField(
        blank=True,
        null=True,
        help_text=_("Should the title be prepended?"),
        verbose_name=_("Prepend?")
    )

    class Meta:
        managed = False
        db_table = "titles"
        ordering = ("title_id",)
        verbose_name = _("Title")
        verbose_name_plural = _("Titles")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        if self.female_text == self.male_text:
            return self.female_text
        return f"F: {self.female_text} - M: {self.male_text}"
