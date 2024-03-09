from django.db import models
from django.contrib import admin

from ishar.apps.mobiles.models.mobile import Mobile


class Challenge(models.Model):
    """Ishar challenge."""
    challenge_id = models.AutoField(
        help_text="Auto-generated, permanent challenge identification number.",
        primary_key=True,
        verbose_name="Challenge ID",
    )
    mobile = models.ForeignKey(
        db_column="mob_vnum",
        to=Mobile,
        to_field="id",
        on_delete=models.DO_NOTHING,
        help_text="Target mobile of the challenge.",
        verbose_name="Mobile"
    )
    max_level = models.IntegerField(
        help_text="Maximum level of the challenge.",
        verbose_name="Maximum Level"
    )
    max_people = models.IntegerField(
        help_text="Maximum number of people for the challenge.",
        verbose_name="Maximum People"
    )
    chall_tier = models.IntegerField(
        help_text="Tier of the challenge.",
        verbose_name="Challenge Tier"
    )
    challenge_desc = models.CharField(
        help_text="Friendly description of the challenge.",
        max_length=80,
        verbose_name="Challenge Description"
    )
    winner_desc = models.CharField(
        help_text=(
            "Description of the winner(s) of the challenge. "
            "Blank indicates that the challenge is not complete."
        ),
        max_length=80,
        verbose_name="Winner Description"
    )
    is_active = models.BooleanField(
        help_text="Is the challenge currently active?",
        verbose_name="Active?"
    )
    last_completion = models.DateTimeField(
        help_text="Date and time when the challenge was last completed.",
        verbose_name="Last Completion"
    )
    num_completed = models.IntegerField(
        help_text="Number of times that the challenge has been completed.",
        verbose_name="Number Completed"
    )
    num_picked = models.IntegerField(
        help_text="Number of times that the challenge has been picked.",
        verbose_name="Number Picked"
    )

    class Meta:
        managed = False
        db_table = "challenges"
        default_related_name = "challenge"
        ordering = ("-is_active", "-winner_desc", "challenge_desc")
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return self.challenge_desc or self.mobile.long_name

    @admin.display(boolean=True, description="Complete?", ordering="winner_desc")
    def is_completed(self):
        """
        Boolean whether challenge has a winner description,
            meaning that the challenge must have been completed.
        """
        if self.winner_desc:
            return True
        return False

    def winners(self) -> list:
        """
        List of winners of a challenge.
        """
        out = []
        winners = self.winner_desc
        if winners:
            if ',' in winners:
                for winner in winners.split(','):
                    out.append(winner.strip())
            else:
                out.append(winners)
        return out
