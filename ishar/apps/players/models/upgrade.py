from django.db import models

from ishar.apps.players.models import Player


class RemortUpgrade(models.Model):
    """
    Remort Upgrade.
    """
    upgrade_id = models.PositiveIntegerField(
        help_text=(
            "Auto-generated, permanent identification number of the "
            "remort upgrade."
        ),
        primary_key=True,
        verbose_name="Upgrade ID"
    )
    name = models.CharField(
        help_text="Name of the remort upgrade.",
        max_length=20,
        unique=True,
        verbose_name="Name"
    )
    renown_cost = models.PositiveSmallIntegerField(
        help_text="Renown cost of the remort upgrade.",
        verbose_name="Renown Cost"
    )
    max_value = models.PositiveSmallIntegerField(
        help_text="Maximum value of the remort upgrade.",
        verbose_name="Maximum Value"
    )
    scale = models.IntegerField(
        help_text="Scale of the remort upgrade.",
        verbose_name="Scale"
    )
    display_name = models.CharField(
        help_text="Display name of the remort upgrade.",
        max_length=30,
        verbose_name="Display Name"
    )
    can_buy = models.BooleanField(
        help_text="Whether the remort upgrade can be bought.",
        verbose_name="Can Buy?"
    )
    bonus = models.IntegerField(
        help_text="Bonus of the remort upgrade.",
        verbose_name="Bonus"
    )
    survival_scale = models.IntegerField(
        help_text="Scale of the remort upgrade, for survival players.",
        verbose_name="Survival Scale"
    )
    survival_renown_cost = models.IntegerField(
        help_text="Renown cost of the remort upgrade, for survival players.",
        verbose_name="Survival Renown Cost"
    )

    class Meta:
        db_table = "remort_upgrades"
        default_related_name = "upgrade"
        managed = False
        ordering = ("-can_buy", "display_name")
        verbose_name = "Remort Upgrade"
        verbose_name_plural = "Remort Upgrades"

    def __repr__(self):
        return f"{self.__class__.__name__}: {repr(self.__str__())}"

    def __str__(self):
        return self.display_name


class PlayerRemortUpgrade(models.Model):
    """
    Player relation to a remort upgrade.
    """
    player = models.ForeignKey(
        primary_key=True,  # Fake it, just so reads work.
        db_column="player_id",
        editable=False,
        related_query_name="remort_upgrade",
        related_name="all_remort_upgrades",
        to=Player,
        to_field="id",
        on_delete=models.CASCADE,
        help_text="Player with a remort upgrade.",
        verbose_name="Player"
    )
    upgrade = models.ForeignKey(
        db_column="upgrade_id",
        editable=False,
        to=RemortUpgrade,
        to_field="upgrade_id",
        related_query_name="+",
        on_delete=models.CASCADE,
        help_text="Remort upgrade affecting a player.",
        verbose_name="Remort Upgrade"
    )
    value = models.PositiveIntegerField(
        blank=False,
        default=0,
        null=False,
        help_text="Value of a player's remort upgrade.",
        verbose_name="Value"
    )
    essence_perk = models.BooleanField(
        help_text="Is the player's remort upgrade an essence perk?",
        verbose_name="Essence Perk?"
    )

    class Meta:
        managed = False
        db_table = "player_remort_upgrades"
        ordering = ("upgrade", "player")
        unique_together = (("upgrade", "player"),)
        verbose_name = "Player's Remort Upgrade"
        verbose_name_plural = "Player's Remort Upgrades"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {repr(self.__str__())}"
        )

    def __str__(self) -> str:
        return f"{self.upgrade} @ {self.player} : {self.value}"
