from django.db import models
from django.contrib import admin


class Challenge(models.Model):
    """
    Challenge.
    """
    challenge_id = models.SmallAutoField(
        primary_key=True,
        help_text="Auto-generated permanent challenge identification number.",
        verbose_name="Challenge ID"
    )
    mob_vnum = models.IntegerField(
        help_text="VNUM of the mobile target of the challenge.",
        verbose_name="Mobile VUM"
    )
    orig_level = models.IntegerField(
        help_text="Original level of the challenge.",
        verbose_name="Original Level"
    )
    orig_people = models.IntegerField(
        help_text="Original number of people for the challenge.",
        verbose_name="Original People"
    )
    orig_tier = models.IntegerField(
        help_text="Original tier of the challenge.",
        verbose_name="Original Tier"
    )
    adj_level = models.IntegerField(
        help_text="Adjusted level of the challenge.",
        verbose_name="Adjusted Level"
    )
    adj_people = models.IntegerField(
        help_text="Adjusted number of people for the challenge.",
        verbose_name="Adjusted People"
    )
    adj_tier = models.IntegerField(
        help_text="Adjusted tier of the challenge.",
        verbose_name="Adjusted Tier"
    )
    challenge_desc = models.CharField(
        max_length=80,
        help_text="Friendly description of the challenge.",
        verbose_name="Challenge Description"
    )
    winner_desc = models.CharField(
        max_length=80,
        help_text="Description of the winner(s) of the challenge.",
        verbose_name="Winner Description"
    )
    mob_name = models.CharField(
        max_length=30,
        help_text="Name of the mobile target of the challenge.",
        verbose_name="Mobile Name"
    )
    is_active = models.BooleanField(
        help_text="Is the challenge currently active?",
        verbose_name="Is Active?"
    )

    class Meta:
        managed = False
        db_table = "challenges"
        default_related_name = "challenge"
        ordering = ("-is_active", "-winner_desc", "challenge_desc")
        verbose_name = "Challenge"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}: {repr(self.__str__())} "
            f"({self.challenge_id})"
        )

    def __str__(self):
        return self.challenge_desc or self.mob_name or self.challenge_id

    @admin.display(
        boolean=True, description="Completed?", ordering="winner_desc"
    )
    def _is_completed(self):
        """
        Boolean whether challenge is completed.
        """
        if self.winner_desc != '' and self.winner_desc != "'--'":
            return True
        return False
