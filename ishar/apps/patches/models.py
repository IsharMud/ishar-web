import os

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from ishar.apps.accounts.models import Account


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
        upload_to=settings.PATCHES_URL,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])]
    )
    is_visible = models.BooleanField(
        default=True,
        help_text="Should the patch be visible publicly?",
        verbose_name="Visible?"
    )

    class Meta:
        managed = True
        db_table = "patches"
        default_related_name = "patch"
        ordering = ("-patch_date",)
        verbose_name = "Patch"
        verbose_name_plural = "Patches"

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__, self.__str__(), self.pk
        )

    def __str__(self):
        return self.patch_name


@receiver(models.signals.post_delete, sender=Patch)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Delete old patch PDF from file-system when Patch object is deleted."""
    if instance.patch_file:
        if os.path.isfile(instance.patch_file.path):
            os.remove(instance.patch_file.path)


@receiver(models.signals.pre_save, sender=Patch)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Delete old patch PDF from file-system when Patch object is updated."""
    if not instance.pk:
        return False

    try:
        old_file = Patch.objects.get(pk=instance.pk).patch_file
    except Patch.DoesNotExist:
        return False

    new_file = instance.patch_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
