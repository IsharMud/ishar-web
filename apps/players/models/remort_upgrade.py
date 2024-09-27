from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.skills.models.skill import Skill


class RemortUpgradeManager(models.Manager):
    def get_by_natural_key(self, name):
        """Natural key is remort upgrade name."""
        return self.get(name=name)


class RemortUpgrade(models.Model):
    """Ishar remort upgrade."""
    objects = RemortUpgradeManager()

    upgrade_id = models.AutoField(
        help_text=_(
            "Auto-generated, permanent identification number of the remort "
            "upgrade."
        ),
        primary_key=True,
        verbose_name=_("Upgrade ID")
    )
    name = models.CharField(
        help_text=_("Name of the remort upgrade."),
        max_length=20,
        unique=True,
        verbose_name=_("Name")
    )
    renown_cost = models.PositiveSmallIntegerField(
        help_text=_("Renown cost of the remort upgrade."),
        verbose_name=_("Renown Cost")
    )
    max_value = models.PositiveSmallIntegerField(
        help_text=_("Maximum value of the remort upgrade."),
        verbose_name=_("Maximum Value")
    )
    scale = models.IntegerField(
        help_text=_("Scale of the remort upgrade."),
        verbose_name=_("Scale")
    )
    display_name = models.CharField(
        help_text=_("Display name of the remort upgrade."),
        max_length=30,
        verbose_name=_("Display Name")
    )
    can_buy = models.BooleanField(
        help_text=_("Whether the remort upgrade can be bought."),
        verbose_name=_("Can Buy?")
    )
    bonus = models.IntegerField(
        help_text=_("Bonus of the remort upgrade."),
        verbose_name=_("Bonus")
    )
    survival_scale = models.IntegerField(
        help_text=_("Scale of the remort upgrade, for survival players."),
        verbose_name=_("Survival Scale")
    )
    survival_renown_cost = models.IntegerField(
        help_text=_("Renown cost of the remort upgrade, for survival players."),
        verbose_name=_("Survival Renown Cost")
    )
    reward_skill = models.ForeignKey(
        to=Skill,
        to_field="id",
        blank=True,
        null=True,
        db_column="reward_skill",
        on_delete=models.DO_NOTHING,
        help_text=_("Skill rewarded by the remort upgrade."),
        verbose_name=_("Reward Skill")
    )

    class Meta:
        db_table = "remort_upgrades"
        default_related_name = "upgrade"
        managed = False
        ordering = ("-can_buy", "display_name")
        verbose_name = _("Remort Upgrade")
        verbose_name_plural = _("Remort Upgrades")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.display_name

    @property
    def anchor(self) -> str:
        return self.name.strip().lower().replace("_", "-")

    def calculate_tiers(self, survival: bool) -> list:
        # Create a list of the cost for each tier of the remort upgrade.
        tiers = []

        # Return the initialized empty list for disabled upgrades.
        if self.can_buy is not True:
            return tiers

        # Calculate with either classic or survival cost and scale.
        max_value = self.max_value
        price = self.renown_cost
        scale = self.scale
        if survival is True:
            price = self.survival_renown_cost
            scale = self.survival_scale

        cost = 0
        value = 0
        while value <= max_value:
            i = 1
            cost += price
            while i <= scale:
                i += 1
                value += 1
                if value > max_value:
                    break
                tiers.append(cost)
        return tiers

    @property
    def survival_tiers(self) -> list:
        return self.calculate_tiers(survival=True)

    @property
    def tiers(self) -> list:
        return self.calculate_tiers(survival=False)

    def natural_key(self) -> str:
        # Natural key is remort upgrade name.
        return self.name
