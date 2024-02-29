from django.db import models


class PlayerFlag(models.Model):
    """
    Player Flag.
    """
    flag_id = models.PositiveIntegerField(
        db_column="flag_id",
        primary_key=True,
        help_text="Auto-generated identification number of the player flag.",
        verbose_name="Player Flag ID"
    )
    name = models.CharField(
        blank=False,
        db_column="name",
        max_length=20,
        null=False,
        help_text="Name of the player flag.",
        unique=True,
        verbose_name="Name"
    )

    class Meta:
        managed = False
        db_table = "player_flags"
        ordering = ("name", "flag_id")
        verbose_name = "Player/Mobile Flag"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.flag_id
        )

    def __str__(self) -> str:
        return self.name
