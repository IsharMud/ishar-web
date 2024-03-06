from django.db import models
from django.utils.translation import gettext_lazy as _


class RemortUpgrade(models.Model):
    """
    Remort Upgrade.
    """
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

    class Meta:
        db_table = "remort_upgrades"
        default_related_name = "upgrade"
        managed = False
        ordering = ("-can_buy", "display_name")
        verbose_name = _("Remort Upgrade")
        verbose_name_plural = _("Remort Upgrades")

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__, self.__str__(), self.pk
        )

    def __str__(self):
        return self.display_name
