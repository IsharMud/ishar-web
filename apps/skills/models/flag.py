from django.db import models


class SpellFlag(models.Model):
    """
    Ishar spell flag.
    """
    id = models.AutoField(
        blank=False,
        editable=False,
        help_text=(
            "Auto-generated permanent identification number for a spell flag."
        ),
        null=False,
        primary_key=True,
        verbose_name="Spell Flag ID"
    )
    name = models.CharField(
        max_length=50,
        help_text="Name of the spell flag.",
        verbose_name="Spell Flag Name"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Description of the spell flag.",
        verbose_name="Spell Flag Description"
    )

    class Meta:
        db_table = "spell_flags"
        managed = False
        ordering = ("name",)
        verbose_name = "Skill Flag"
        verbose_name_plural = "Skill Flags"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.name
