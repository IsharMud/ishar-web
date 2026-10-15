from django.db import models

from apps.accounts.models.account import Account
from apps.skills.models.skill import Skill


class AccountFatedSkill(models.Model):
    """A thread bound to an account's Fated pool (``account_fated_skills``).

    ``skill_level`` is the bound skill level — for a passive, the bound tier.
    ``255`` (``SEVERED``) marks a thread cut for the season: never re-bindable
    and weighing nothing on the loom.
    """

    SEVERED = 255

    account_fated_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated bound-thread ID.",
        verbose_name="Account Fated Skill ID",
    )
    account = models.ForeignKey(
        db_column="account_id",
        on_delete=models.DO_NOTHING,
        related_name="fated_skills",
        related_query_name="fated_skill",
        to=Account,
        help_text="Account whose pool holds the thread.",
        verbose_name="Account",
    )
    skill = models.ForeignKey(
        db_column="skill_id",
        on_delete=models.DO_NOTHING,
        related_name="+",
        to=Skill,
        help_text="The bound skill or spell.",
        verbose_name="Skill",
    )
    skill_level = models.PositiveIntegerField(
        help_text="Bound level (a passive's bound tier); 255 = severed.",
        verbose_name="Skill Level",
    )

    class Meta:
        managed = False
        db_table = "account_fated_skills"
        ordering = ("account", "skill")
        unique_together = (("account", "skill"),)
        verbose_name = "Account Fated Skill"
        verbose_name_plural = "Account Fated Skills"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.skill} @ {self.account}"

    @property
    def is_severed(self) -> bool:
        return self.skill_level == self.SEVERED
