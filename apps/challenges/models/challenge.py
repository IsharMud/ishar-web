from django.db import models
from django.contrib.admin import display
from django.template.defaultfilters import slugify

from apps.mobiles.models.mobile import Mobile
from apps.players.models.player import Player


class ChallengeManager(models.Manager):
    def get_by_natural_key(self, challenge_desc):
        # Natural key by challenge description.
        return self.get(challenge_desc=challenge_desc)


class Challenge(models.Model):
    """Ishar challenge."""
    objects = ChallengeManager()

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
        blank=True,
        help_text=(
            "Description of the winner(s) of the challenge. "
            "Blank indicates that the challenge is not complete."
        ),
        max_length=80,
        null=True,
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
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.challenge_desc or self.mobile.long_name

    def natural_key(self) -> str:
        # Natural key by challenge description.
        return self.challenge_desc

    @display(boolean=True, description="Complete?", ordering="winner_desc")
    def is_completed(self) -> bool:
        # Boolean if challenge has winner description, meaning completed.
        if self.winner_desc:
            return True
        return False

    @property
    def anchor(self) -> str:
        return slugify(self.mobile.long_name).replace("_", "-")

    def winners(self) -> list[str,]:
        # List of players that have won a completed challenge.
        out = []
        winners = self.winner_desc
        if winners:
            if ',' in winners:
                for winner in winners.split(','):
                    out.append(winner.strip())
            else:
                out.append(winners)
        return out

    def winners_links(self) -> list[str,]:
        # List of links to players that have won a completed challenge.
        out = []
        for winner in self.winners():
            try:
                player = Player.objects.get(name=winner)
            except Player.DoesNotExist:
                item = winner
            else:
                item = player.name
                if player.player_link:
                    item = player.player_link
            out.append(item)
        return out
