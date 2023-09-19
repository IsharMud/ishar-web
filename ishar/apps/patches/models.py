from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from ..accounts.models import Account


class Patch(models.Model):
    """
    Patch.
    """
    patch_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated, permanent ID number of the patch.",
        verbose_name="Patch ID"
    )
    account = models.ForeignKey(
        to=Account,
        on_delete=models.DO_NOTHING,
        help_text="Account responsible for the patch.",
        verbose_name="Account"
    )
    patch_date = models.DateTimeField(
        default=timezone.now,
        help_text="Date and time of the patch to sort/display on the website.",
        verbose_name="Patch Date"
    )
    patch_name = models.CharField(
        max_length=64,
        unique=True,
        help_text="Name of the patch.",
        verbose_name="Patch Name"
    )
    patch_file = models.FileField(
        max_length=100,
        help_text="PDF file of the patch.",
        verbose_name="Patch File",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    is_visible = models.BooleanField(
        default=True,
        help_text="Should the patch be visible publicly?",
        verbose_name="Is Visible?"
    )

    class Meta:
        managed = True
        db_table = "patches"
        ordering = ("-patch_date",)
        verbose_name = "Patch"
        verbose_name_plural = "Patches"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}: "
            f"{repr(self.__str__())} @ {self.patch_date} ({self.patch_id})"
        )

    def __str__(self):
        return self.patch_name
