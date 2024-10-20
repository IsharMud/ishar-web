from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class ObjectMod(models.Model):
    """Ishar object mod."""

    mod_id = models.AutoField(
        help_text=_("Primary key identification number of object mod."),
        primary_key=True,
        verbose_name=_("Mod ID"),
    )
    name = models.CharField(
        help_text=_("Name of the object mod."),
        max_length=30,
        unique=True,
        verbose_name=_("Name"),
    )
    created_at = models.DateTimeField(
        help_text=_("Date and time when the object mod was created."),
        verbose_name=_("Created At"),
    )
    updated_at = models.DateTimeField(
        help_text=_("Date and time when the object mod was updated."),
        verbose_name=_("Updated At"),
    )

    class Meta:
        managed = False
        db_table = "object_mods"
        default_related_name = "mod"
        ordering = ("name",)
        verbose_name = _("Object Mod")
        verbose_name_plural = _("Object Mods")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.name

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
