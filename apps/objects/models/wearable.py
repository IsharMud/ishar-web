from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .object import Object


class ObjectWearableFlag(models.Model):
    """Ishar object wearable flag."""

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
    take = models.BooleanField(
        db_column='TAKE',
        help_text=_('"TAKE" wearable flag of the object.'),
        verbose_name=_("Take")
    )
    wield = models.BooleanField(
        db_column='WIELD',
        help_text=_('"WIELD" wearable flag of the object.'),
        verbose_name=_("Wield")
    )
    hold = models.BooleanField(
        db_column='HOLD',
        help_text=_('"HOLD" wearable flag of the object.'),
        verbose_name=_("Hold")
    )
    two_hands = models.BooleanField(
        db_column='TWO_HANDS',
        help_text=_('"Two Hands" wearable flag of the object.'),
        verbose_name=_("Two Hands")
    )
    body = models.BooleanField(
        db_column='BODY',
        help_text=_('"BODY" wearable flag of the object.'),
        verbose_name=_("Body")
    )
    head = models.BooleanField(
        db_column='HEAD',
        help_text=_('"HEAD" wearable flag of the object.'),
        verbose_name=_("Head")
    )
    neck = models.BooleanField(
        db_column='NECK',
        help_text=_('"NECK" wearable flag of the object.'),
        verbose_name=_("Neck")
    )
    chest = models.BooleanField(
        db_column='CHEST',
        help_text=_('"CHEST" wearable flag of the object.'),
        verbose_name=_("Chest")
    )
    back = models.BooleanField(
        db_column='BACK',
        help_text=_('"WRIST" wearable flag of the object.'),
        verbose_name=_("Wrist")
    )
    arms = models.BooleanField(
        db_column='ARMS',
        help_text=_('"ARMS" wearable flag of the object.'),
        verbose_name=_("Arms")
    )
    wrist = models.BooleanField(
        db_column='WRIST',
        help_text=_('"WRIST" wearable flag of the object.'),
        verbose_name=_("Wrist")
    )
    hands = models.BooleanField(
        db_column='HANDS',
        help_text=_('"HANDS" wearable flag of the object.'),
        verbose_name=_("Hands")
    )
    finger = models.BooleanField(
        db_column='FINGER',
        help_text=_('"FINGER" wearable flag of the object.'),
        verbose_name=_("Finger")
    )
    waist = models.BooleanField(
        db_column='WAIST',
        help_text=_('"WAIST" wearable flag of the object.'),
        verbose_name=_("Waist")
    )
    legs = models.BooleanField(
        db_column='LEGS',
        help_text=_('"LEGS" wearable flag of the object.'),
        verbose_name=_("Legs")
    )
    feet = models.BooleanField(
        db_column='FEET',
        help_text=_('"FEET" wearable flag of the object.'),
        verbose_name=_("Feet")
    )
    about = models.BooleanField(
        db_column='ABOUT',
        help_text=_('"ABOUT" wearable flag of the object.'),
        verbose_name=_("About")
    )
    shield = models.BooleanField(
        db_column='SHIELD',
        help_text=_('"SHIELD" wearable flag of the object.'),
        verbose_name=_("Shield")
    )
    face = models.BooleanField(
        db_column='FACE',
        help_text=_('"FACE" wearable flag of the object.'),
        verbose_name=_("Face")
    )
    mouth = models.BooleanField(
        db_column='MOUTH',
        help_text=_('"MOUTH" wearable flag of the object.'),
        verbose_name=_("Mouth")
    )
    fore_mark = models.BooleanField(
        db_column='FORE_MARK',
        help_text=_('"FORE_MARK" wearable flag of the object.'),
        verbose_name=_("Fore Mark")
    )
    upper_body = models.BooleanField(
        db_column='UPPER_BODY',
        help_text=_('"UPPER_BODY" wearable flag of the object.'),
        verbose_name=_("Upper Body")
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
        db_table = "object_wearable_flags"
        default_related_name = "wearable_flag"
        ordering = ("-object",)
        verbose_name = _("Object Wearable Flag")
        verbose_name_plural = _("Object Wearable Flags")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        return f"{self._meta.verbose_name} @ {self.object}"

    def save(
            self,
            force_insert=False, force_update=False, using=None,
            update_fields=None
    ):
        if not self.pk:
            self.created_at = now()
        self.updated_at = now()
        super().save(
            force_insert=force_insert, using=using, update_fields=update_fields
        )
