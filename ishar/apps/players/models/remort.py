from django.db import models


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
        managed = False
        ordering = ("-can_buy", "display_name",)
        verbose_name = "Remort Upgrade"

    def __repr__(self):
        return f"{self.__class__.__name__}: {repr(self.__str__())}"

    def __str__(self):
        return self.display_name
