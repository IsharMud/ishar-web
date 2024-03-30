from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ishar.apps.core.models.affect_flag import AffectFlag

from .object import Object


class ObjectAffectFlag(models.Model):
    """Ishar object affect flag."""
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
    affect_flag = models.OneToOneField(
        to=AffectFlag,
        on_delete=models.DO_NOTHING,
        help_text=_("Affect flag affecting the object."),
        related_name="+",
        verbose_name=_("Affect Flag")
    )
    value = models.IntegerField(
        help_text=_("Value of the object affect flag."),
        verbose_name=_("Value")
    )
    created_at = models.DateTimeField(
        help_text=_("Date and time when the object flag was created."),
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        help_text=_("Date and time when the object flag was updated."),
        verbose_name=_("Updated At")
    )

    class Meta:
        managed = False
        db_table = "object_affect_flags"
        default_related_name = "affect_flag"
        ordering = ("object", "-value")
        unique_together = (("affect_flag", "object"),)
        verbose_name = "Object Affect Flag"
        verbose_name_plural = "Object Affect Flags"

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
