from django.db import models


class TensionModifier(models.Model):
    """One knot on the loom's menu (``tension_modifiers``, game-owned).

    Rows group into families: one rule axis each, tiers strictly harsher at
    strictly higher weight. A tier's weight is the whole knot's weight, not an
    increment — only one tier of a family can be tied. ``modifier_id`` is
    positional: a knot is tied on a life when
    ``players.knots_mask & (1 << (modifier_id - 1))``. Menu order is id
    order: the seed inserts each family's tiers together, ascending.
    """

    modifier_id = models.AutoField(
        primary_key=True,
        help_text="Knot ID; bit (modifier_id - 1) of a player's knots_mask.",
        verbose_name="Modifier ID",
    )
    effect_key = models.CharField(
        max_length=40,
        help_text="Machine effect the game audits at boot.",
        verbose_name="Effect Key",
    )
    family = models.CharField(
        max_length=40,
        help_text="Rule axis; one tier per family can be tied.",
        verbose_name="Family",
    )
    tier = models.SmallIntegerField(
        default=1,
        help_text="Tier within the family, harsher upward.",
        verbose_name="Tier",
    )
    magnitude = models.IntegerField(
        help_text="Effect magnitude; meaning depends on the effect key.",
        verbose_name="Magnitude",
    )
    weight = models.IntegerField(
        help_text="Knot weight in integer tenths (20 = 2.0).",
        verbose_name="Weight",
    )
    name = models.CharField(
        max_length=80,
        help_text="Player-facing knot name.",
        verbose_name="Name",
    )
    description = models.CharField(
        max_length=255,
        help_text="Player-facing rule text.",
        verbose_name="Description",
    )
    secondary_effect_key = models.CharField(
        blank=True,
        max_length=40,
        null=True,
        help_text="Optional second machine effect carried by the same knot.",
        verbose_name="Secondary Effect Key",
    )
    secondary_magnitude = models.IntegerField(
        blank=True,
        null=True,
        help_text="Magnitude of the secondary effect.",
        verbose_name="Secondary Magnitude",
    )

    class Meta:
        managed = False
        db_table = "tension_modifiers"
        default_related_name = "tension_modifier"
        ordering = ("modifier_id",)
        verbose_name = "Tension Modifier"
        verbose_name_plural = "Tension Modifiers"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.name

    @property
    def bit(self) -> int:
        return 1 << (self.modifier_id - 1)

    @property
    def weight_display(self) -> str:
        from ..tension import tenths

        return tenths(self.weight)
