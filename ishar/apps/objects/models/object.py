from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ishar.apps.skills.models.skill import Skill

from .type import ObjectType


class ObjectManager(models.Manager):
    def get_by_natural_key(self, longname):
        """Natural key is object long name."""
        return self.get(longname=longname)


class Object(models.Model):
    """Ishar object."""
    objects = ObjectManager()

    vnum = models.AutoField(
        help_text=_(
            'Primary key identification number ("VNUM") of the object.'
        ),
        primary_key=True,
        verbose_name=_('Object ID ("VNUM")')
    )
    name = models.CharField(
        max_length=128,
        blank=True,
        help_text=_("Name of the object."),
        null=True,
        verbose_name=_("Name"),
    )
    longname = models.CharField(
        max_length=256,
        blank=True,
        help_text=_("Long name of the object."),
        null=True,
        verbose_name=_("Long Name")
    )
    appearance = models.CharField(
        max_length=256,
        blank=True,
        help_text=_("Appearance of the object."),
        null=True,
        verbose_name=_("Appearance")
    )
    description = models.CharField(
        max_length=8192,
        blank=True,
        help_text=_("Description of the object."),
        null=True,
        verbose_name=_("Description")
    )
    func = models.CharField(
        max_length=128,
        blank=True,
        help_text=_("Function of the object."),
        null=True,
        verbose_name=_("Function")
    )
    state = models.IntegerField(
        blank=True,
        help_text=_("State of the object."),
        null=True,
        verbose_name=_("State")
    )
    timer = models.SmallIntegerField(
        blank=True,
        help_text=_("Timer for the object."),
        null=True,
        verbose_name=_("Timer")
    )
    enchant = models.ForeignKey(
        blank=True,
        db_column="enchant",
        help_text=_("Enchantment of the object."),
        limit_choices_to=models.Q(parent_skill__skill_name__exact="Enchanting"),
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="+",
        to=Skill,
        to_field="id",
        verbose_name=_("Enchant")
    )
    item_type = models.IntegerField(
        blank=True,
        choices=ObjectType,
        help_text=_("Item type of the object."),
        null=True,
        verbose_name=_("Item Type")
    )
    equipped = models.PositiveIntegerField(
        blank=True,
        help_text=_("Equipped integer for the object."),
        null=True,
        verbose_name=_("Equipped")
    )
    size = models.SmallIntegerField(
        blank=True,
        help_text=_("Size of the object."),
        null=True,
        verbose_name=_("Size")
    )
    weight = models.IntegerField(
        blank=True,
        help_text=_("Weight of the object."),
        null=True,
        verbose_name=_("Weight")
    )
    value = models.IntegerField(
        blank=True,
        help_text=_("Value of the object."),
        null=True,
        verbose_name=_("Value")
    )
    val0 = models.IntegerField(
        blank=True,
        help_text=_("Value zero (0) of the object."),
        null=True,
        verbose_name=_("Value Zero (0)")
    )
    val1 = models.IntegerField(
        blank=True,
        help_text=_("Value one (1) of the object."),
        null=True,
        verbose_name=_("Value One (1)")
    )
    val2 = models.IntegerField(
        blank=True,
        help_text=_("Value two (2) of the object."),
        null=True,
        verbose_name=_("Value Two (2)")
    )
    val3 = models.IntegerField(
        blank=True,
        help_text=_("Value three (3) of the object."),
        null=True,
        verbose_name=_("Value Three (3)")
    )
    deleted = models.BooleanField(
        help_text=_("Is the object deleted?"),
        verbose_name=_("Deleted?")
    )
    created_at = models.DateTimeField(
        help_text=_("Date and time when the object was created."),
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        help_text=_("Date and time when the object was updated."),
        verbose_name=_("Updated At")
    )

    class Meta:
        managed = False
        db_table = "objects"
        default_related_name = "object"
        ordering = ("vnum",)
        verbose_name = "Object"
        verbose_name_plural = "Objects"

    def __repr__(self) -> str:
        return "%s: %s" % (
            self.__class__.__name__,
            self.__str__(),
        )

    def __str__(self) -> str:
        return "%i. %s" % (
            self.pk,
            self.longname or self.name
        )

    def natural_key(self) -> str:
        """Natural key is object long name."""
        return self.longname

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
