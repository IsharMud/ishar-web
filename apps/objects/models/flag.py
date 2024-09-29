from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .object import Object


class ObjectFlag(models.Model):
    """Ishar object flag."""
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
    magic = models.BooleanField(
        db_column="MAGIC",
        help_text=_('"MAGIC" flag of the object.'),
        verbose_name=_("Magic")
    )
    cursed = models.BooleanField(
        db_column="CURSED",
        help_text=_('"CURSED" flag of the object.'),
        verbose_name=_("Cursed")
    )
    donated = models.BooleanField(
        db_column="DONATED",
        help_text=_('"DONATED" flag of the object.'),
        verbose_name=_("Donated")
    )
    notgood = models.BooleanField(
        db_column="NOTGOOD",
        help_text=_('"NOTGOOD" flag of the object.'),
        verbose_name=_("Not Good")
    )
    notevil = models.BooleanField(
        db_column="NOTEVIL",
        help_text=_('"NOTEVIL" flag of the object.'),
        verbose_name=_("Not Evil")
    )
    notneutral = models.BooleanField(
        db_column="NOTNEUTRAL",
        help_text=_('"NOTNEUTRAL" flag of the object.'),
        verbose_name=_("Not Neutral")
    )
    invisible = models.BooleanField(
        db_column="INVISIBLE",
        help_text=_('"INVISIBLE" flag of the object.'),
        verbose_name=_("Invisible")
    )
    moved = models.BooleanField(
        db_column="MOVED",
        help_text=_('"MOVED" flag of the object.'),
        verbose_name=_("Moved")
    )
    notwarrior = models.BooleanField(
        db_column="NOTWARRIOR",
        help_text=_('"NOTWARRIOR" flag of the object.'),
        verbose_name=_("Not Warrior")
    )
    notrogue = models.BooleanField(
        db_column="NOTROGUE",
        help_text=_('"NOTROGUE" flag of the object.'),
        verbose_name=_("Not Rogue")
    )
    notcleric = models.BooleanField(
        db_column="NOTCLERIC",
        help_text=_('"NOTCLERIC" flag of the object.'),
        verbose_name=_("Not Cleric")
    )
    notmagician = models.BooleanField(
        db_column="NOTMAGICIAN",
        help_text=_('"NOTMAGICIAN" flag of the object.'),
        verbose_name=_("Not Magician")
    )
    not_shaman = models.BooleanField(
        db_column="NOT_SHAMAN",
        help_text=_('"NOT_SHAMAN" flag of the object.'),
        verbose_name=_("Not Shaman")
    )
    trapped = models.BooleanField(
        db_column="TRAPPED",
        help_text=_('"TRAPPED" flag of the object.'),
        verbose_name=_("Trapped")
    )
    surface = models.BooleanField(
        db_column="SURFACE",
        help_text=_('"SURFACE" flag of the object.'),
        verbose_name=_("Surface")
    )
    high_rent = models.BooleanField(
        db_column="HIGH_RENT",
        help_text=_('"HIGH_RENT" flag of the object.'),
        verbose_name=_("High Rent")
    )
    notmortals = models.BooleanField(
        db_column="NOTMORTALS",
        help_text=_('"NOTMORTALS" flag of the object.'),
        verbose_name=_("Not Mortals")
    )
    day_decay = models.BooleanField(
        db_column="DAY_DECAY",
        help_text=_('"DAY_DECAY" flag of the object.'),
        verbose_name=_("Day Decay")
    )
    enchanted = models.BooleanField(
        db_column="ENCHANTED",
        help_text=_('"ENCHANTED" flag of the object.'),
        verbose_name=_("Enchanted")
    )
    rented = models.BooleanField(
        db_column="RENTED",
        help_text=_('"RENTED" flag of the object.'),
        verbose_name=_("Rented")
    )
    possessed = models.BooleanField(
        db_column="POSSESSED",
        help_text=_('"POSSESSED" flag of the object.'),
        verbose_name=_("Possessed")
    )
    persistent = models.BooleanField(
        db_column="PERSISTENT",
        help_text=_('"PERSISTENT" flag of the object.'),
        verbose_name=_("Persistent")
    )
    modified = models.BooleanField(
        db_column="MODIFIED",
        help_text=_('"MODIFIED" flag of the object.'),
        verbose_name=_("Modified")
    )
    in_edit = models.BooleanField(
        db_column="IN_EDIT",
        help_text=_('"IN_EDIT" flag of the object.'),
        verbose_name=_("In Edit")
    )
    remove_obj = models.BooleanField(
        db_column="REMOVE_OBJ",
        help_text=_('"REMOVE_OBJ" flag of the object.'),
        verbose_name=_("Remove OBJ")
    )
    controlled = models.BooleanField(
        db_column="CONTROLLED",
        help_text=_('"CONTROLLED" flag of the object.'),
        verbose_name=_("Controlled")
    )
    noident = models.BooleanField(
        db_column="NOIDENT",
        help_text=_('"NOIDENT" flag of the object.'),
        verbose_name=_("No Ident")
    )
    unrentable = models.BooleanField(
        db_column="UNRENTABLE",
        help_text=_('"UNRENTABLE" flag of the object.'),
        verbose_name=_("Unrentable")
    )
    nolocate = models.BooleanField(
        db_column="NOLOCATE",
        help_text=_('"NOLOCATE" flag of the object.'),
        verbose_name=_("No Locate")
    )
    artifact = models.BooleanField(
        db_column="ARTIFACT",
        help_text=_('"ARTIFACT" flag of the object.'),
        verbose_name=_("Artifact")
    )
    quest_obj = models.BooleanField(
        db_column="QUEST_OBJ",
        help_text=_('"QUEST_OBJ" flag of the object.'),
        verbose_name=_("Quest Object")
    )
    emp_enchant = models.BooleanField(
        db_column="EMP_ENCHANT",
        help_text=_('"EMP_ENCHANT" flag of the object.'),
        verbose_name=_("Emp Enchant")
    )
    quest_source = models.BooleanField(
        db_column="QUEST_SOURCE",
        help_text=_('"QUEST_SOURCE" flag of the object.'),
        verbose_name=_("Quest Source")
    )
    relic = models.BooleanField(
        db_column="RELIC",
        help_text=_('"RELIC" flag of the object.'),
        verbose_name=_("Relic")
    )
    memory = models.BooleanField(
        db_column="MEMORY",
        help_text=_('"MEMORY" flag of the object.'),
        verbose_name=_("Memory")
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
        db_table = "object_flags"
        default_related_name = "flag"
        ordering = ("-object",)
        verbose_name = "Object Flag"
        verbose_name_plural = "Object Flags"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        return f"{self._meta.verbose_name} @ {self.object}"

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
