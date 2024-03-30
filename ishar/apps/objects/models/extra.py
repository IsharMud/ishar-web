from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..models.object import Object


class ObjectExtra(models.Model):
    """Ishar object extra."""
    object = models.OneToOneField(
        db_column="object_vnum",
        help_text=_(
            'Primary key identification number ("VNUM") of the object.'
        ),
        on_delete=models.DO_NOTHING,
        primary_key=True,
        to=Object,
        to_field="vnum",
        verbose_name=_('Object ID ("VNUM")')
    )
    keywords = models.CharField(
        help_text=_("Keywords of the object extra."),
        max_length=128,
        verbose_name=_("Keywords")
    )
    description = models.CharField(
        help_text=_("Description of the object extra."),
        max_length=4096,
        verbose_name=_("Description")
    )
    created_at = models.DateTimeField(
        help_text=_("Date and time when the object extra was created."),
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        help_text=_("Date and time when the object extra was updated."),
        verbose_name=_("Updated At")
    )

    class Meta:
        managed = False
        db_table = "object_extras"
        default_related_name = "extra"
        ordering = ("-object",)
        verbose_name = "Object Extra"
        verbose_name_plural = "Object Extras"

    def __repr__(self) -> str:
        return "%s: %s" % (
            self.__class__.__name__,
            self.__str__()
        )

    def __str__(self) -> str:
        return "%s @ %s" % (
            self._meta.verbose_name,
            self.object,
        )

    def save(
        self,
        force_insert=False, force_update=False, using=None, update_fields=None
    ):
        now = timezone.now()
        if not self.pk:
            self.created_at = now
        self.updated_at = now
        super().save(
            force_insert=force_insert, using=using, update_fields=update_fields
        )
