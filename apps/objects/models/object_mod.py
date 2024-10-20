from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .mod import ObjectMod
from .object import Object


class ObjectObjectMod(models.Model):
    """Ishar object object mod."""

    object = models.OneToOneField(
        db_column="object_vnum",
        editable=False,
        help_text=_(
            'Primary key identification number ("VNUM") of the object.'
        ),
        on_delete=models.DO_NOTHING,
        primary_key=True,
        related_query_name="+",
        to=Object,
        to_field="vnum",
        verbose_name=_('Object ID ("VNUM")'),
    )
    mod_slot = models.PositiveIntegerField(
        help_text=_("Mod slot of the object mod."),
        verbose_name=_("Mod Slot")
    )
    object_mod = models.ForeignKey(
        editable=False,
        help_text=_("Mod relating to the object."),
        to=ObjectMod,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Object Mod"),
    )
    value = models.IntegerField(
        help_text=_("Value of the object's object mod."),
        verbose_name=_("Value")
    )
    created_at = models.DateTimeField(
        help_text=_("Date and time when the object mod relation was created."),
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        help_text=_("Date and time when the object mod relation was updated."),
        verbose_name=_("Updated At"),
    )

    class Meta:
        managed = False
        db_table = "object_object_mods"
        default_related_name = "object_mod"
        ordering = ("-object", "mod_slot")
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("object", "mod_slot",),
                name="one_slot_per_object"
            ),
        )
        unique_together = (("object", "mod_slot"),)
        verbose_name = _("Object's Mod")
        verbose_name_plural = _("Object's Mods")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        return f"{self.object_mod} (Slot: {self.mod_slot}) @ {self.object}"

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if not self.pk:
            self.created_at = now()

        self.updated_at = now()

        super().save(
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )
