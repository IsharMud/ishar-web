from django.db import models


class PlayerFlagManager(models.Manager):
    def get_by_natural_key(self, name):
        # Natural key of the flag name.
        return self.get(name=name)


class PlayerFlag(models.Model):
    """Ishar player flag, used by both mobiles and players."""
    objects = PlayerFlagManager()

    flag_id = models.AutoField(
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

    def natural_key(self) -> str:
        # Natural key of the flag name.
        return self.name
