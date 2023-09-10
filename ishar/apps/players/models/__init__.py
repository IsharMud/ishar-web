from django.contrib import admin
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


from ...accounts.models import Account
from ....util.ip import dec2ip
from ....util.level import get_immortal_level, get_immortal_type


class Player(models.Model):
    """
    Player character.
    """
    account = models.ForeignKey(
        to=Account,
        on_delete=models.CASCADE,
        related_query_name="player",
        related_name="players",
        help_text="Account that owns the player character.",
        verbose_name="Account"
    )
    name = models.CharField(
        unique=True,
        max_length=15,
        help_text="Name of the player character.",
        verbose_name="Name"
    )
    create_ident = models.CharField(
        max_length=10,
        help_text="Ident that created the player.",
        verbose_name="Create IDENT"
    )
    last_isp = models.CharField(
        max_length=30,
        help_text="Last Internet Service Provider (ISP) to join as the player.",
        verbose_name="Create IDENT"
    )
    description = models.CharField(
        max_length=240, blank=True, null=True,
        help_text="User-written in-game player description.",
        verbose_name="Description"
    )
    title = models.CharField(
        max_length=45,
        help_text="User-selectable player title.",
        verbose_name="Title"
    )
    poofin = models.CharField(
        max_length=80,
        help_text="String displayed upon player poof in.",
        verbose_name="Poof In"
    )
    poofout = models.CharField(
        max_length=80,
        help_text="String displayed upon player poof out.",
        verbose_name="Poof In"
    )
    bankacc = models.PositiveIntegerField(
        help_text="Bank account balance.",
        verbose_name="Bank Account"
    )
    logon_delay = models.PositiveSmallIntegerField(
        help_text="Delay when logging on.",
        verbose_name="Logon Delay"
    )
    true_level = models.PositiveIntegerField(
        help_text="True level of the player character.",
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=max(settings.IMMORTAL_LEVELS)[0])
        ],
        verbose_name="True Level"
    )
    renown = models.PositiveIntegerField(
        help_text="Amount of renown available for the player to spend.",
        verbose_name="Renown"
    )
    remorts = models.PositiveIntegerField(
        help_text="Number of times that the player has remorted.",
        verbose_name="Remorts"
    )
    favors = models.PositiveIntegerField(
        help_text="Amount of favors for the player.",
        verbose_name="Favors"
    )
    online = models.IntegerField(
        blank=True,
        null=True,
        help_text="Amount of time spent logged in to the game, in seconds.",
        verbose_name="Online"
    )
    bound_room = models.PositiveIntegerField(
        help_text="Room ID number where the player is bound.",
        verbose_name="Bound Room"
    )
    load_room = models.PositiveIntegerField(
        help_text="Room ID number where the player is loaded.",
        verbose_name="Load Room"
    )
    invstart_level = models.IntegerField(
        blank=True,
        null=True,
        help_text="Invisible Start Level.",
        verbose_name="Invisible Start Level"
    )
    login_failures = models.PositiveSmallIntegerField(
        help_text="Number of login failures.",
        verbose_name="Login Failures"
    )
    create_haddr = models.IntegerField(
        help_text="HADDR that created the player.",
        verbose_name="Create HADDR"
    )
    login_fail_haddr = models.IntegerField(
        blank=True,
        null=True,
        help_text="HADDR that last failed to log in to the player.",
        verbose_name="Login Fail HADDR"
    )
    last_haddr = models.IntegerField(
        blank=True,
        null=True,
        help_text="Last HADDR to join as the player.",
        verbose_name="Last HADDR"
    )
    last_ident = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Last ident to join as the player.",
        verbose_name="Last IDENT"
    )
    load_room_next = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Load Room Next.",
        verbose_name="Load Room Next"
    )
    load_room_next_expires = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Load Room Next Expires.",
        verbose_name="Load Room Next Expires"
    )
    aggro_until = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Aggro Until.",
        verbose_name="Aggro Until"
    )
    inn_limit = models.PositiveSmallIntegerField(
        help_text="Inn Limit.",
        verbose_name="Inn Limit"
    )
    held_xp = models.IntegerField(
        blank=True,
        null=True,
        help_text="Held XP.",
        verbose_name="Held XP"
    )
    last_isp_change = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Last Internet Service Provider (ISP) change.",
        verbose_name="Last ISP Change"
    )
    is_deleted = models.BooleanField(
        blank=False,
        default=0,
        null=False,
        help_text="Is the player character deleted?",
        verbose_name="Is Deleted?"
    )
    deaths = models.PositiveSmallIntegerField(
        help_text="Number of times that the player has died.",
        verbose_name="Deaths"
    )
    total_renown = models.PositiveSmallIntegerField(
        help_text="Total amount of renown earned by the player.",
        verbose_name="Total Renown"
    )
    quests_completed = models.PositiveSmallIntegerField(
        help_text="Total number of quests completed by the player.",
        verbose_name="Quests Completed"
    )
    challenges_completed = models.PositiveSmallIntegerField(
        help_text="Total number of challenges completed by the player.",
        verbose_name="Challenges Completed"
    )
    game_type = models.IntegerField(
        help_text="Player game type.",
        verbose_name="Game Type",
        choices=settings.GAME_TYPES
    )
    birth = models.DateTimeField(
        help_text="Date and time that the player was created.",
        verbose_name="Birth"
    )
    logon = models.DateTimeField(
        help_text="Date and time that the player last logged on.",
        verbose_name="Log On"
    )
    logout = models.DateTimeField(
        help_text="Date and time that the player last logged out.",
        verbose_name="Log Out"
    )

    class Meta:
        managed = False
        db_table = "players"
        default_related_name = "player"
        ordering = ("-true_level", "id")
        verbose_name = "Player"

    def __repr__(self) -> str:
        return (
            f"Player: {repr(self.__str__())} ({self.id}) [{self.player_type}]'"
        )

    def __str__(self) -> str:
        return self.name

    @property
    @admin.display(description="Create IP", ordering="create_haddr")
    def _create_haddr(self):
        """
        IP address that created the account.
        """
        return dec2ip(self.create_haddr)

    @property
    @admin.display(description="Login Fail IP", ordering="login_fail_haddr")
    def _login_fail_haddr(self):
        """
        Last IP address that failed to log in to the account.
        """
        return dec2ip(self.login_fail_haddr)

    @property
    @admin.display(description="Last IP", ordering="last_haddr")
    def _last_haddr(self):
        """
        Last IP address that logged in to the account.
        """
        return dec2ip(self.last_haddr)

    @admin.display(boolean=True, description="Consort?", ordering="-true_level")
    def is_consort(self) -> bool:
        """
        Boolean whether player is consort, or above.
        """
        return self.is_immortal_type(immortal_type="Consort")

    @admin.display(boolean=True, description="Eternal?", ordering="-true_level")
    def is_eternal(self) -> bool:
        """
        Boolean whether player is eternal, or above.
        """
        return self.is_immortal_type(immortal_type="Eternal")

    @admin.display(boolean=True, description="Forger??", ordering="-true_level")
    def is_forger(self) -> bool:
        """
        Boolean whether player is consort, or above.
        """
        return self.is_immortal_type(immortal_type="Forger")

    @admin.display(boolean=True, description="God?", ordering="-true_level")
    def is_god(self) -> bool:
        """
        Boolean whether player is a "God".
        """
        return self.is_immortal_type(immortal_type="God")

    @admin.display(boolean=True, description="Immortal?", ordering="-true_level")
    def is_immortal(self) -> bool:
        """
        Boolean whether player is immortal, or above, but not consort.
        """
        return self.is_immortal_type(immortal_type="Immortal")

    def is_immortal_type(self, immortal_type="Immortal") -> bool:
        """
        Boolean whether player is an immortal of a certain type, or above.
        """
        if self.true_level >= get_immortal_level(immortal_type=immortal_type):
            return True
        return False

    @admin.display(boolean=True, description="Survival?", ordering='-game_type')
    def is_survival(self) -> bool:
        """
        Boolean whether player is Survival ("perm-death").
        """
        if self.game_type == 1:
            return True
        return False

    @property
    @admin.display(boolean=False, description="Level", ordering='true_level')
    def level(self) -> int:
        return self.true_level

    @property
    def player_stats(self) -> dict:
        """
        Player stats.
        """

        # Start with empty dictionary.
        stats = {}

        # Immortals have no stats.
        if self.is_immortal:
            return stats

        # No stats for mortal players below level five (5),
        #   with less than one (1) hour of play-time
        if self.true_level < 5 and self.online < 3600:
            return stats

        # TODO: PlayerCommon

        # Otherwise, get the players actual stats
        players_stats = {
            'Agility': self.common.agility,
            'Endurance': self.common.endurance,
            'Focus': self.common.focus,
            'Perception': self.common.perception,
            'Strength': self.common.strength,
            'Willpower': self.common.willpower
        }

        # Put the players stats in the appropriate order,
        #   based on their class, and return them
        for stat_order in self.common.player_class.stats_order:
            stats[stat_order] = players_stats[stat_order]
        return stats

    @property
    def immortal_type(self) -> (str, None):
        """
        Type of immortal.
        Returns one of settings.IMMORTAL_LEVELS tuple text values,
            from settings.IMMORTAL_LEVELS, or None.
        """
        return get_immortal_type(level=self.true_level)

    def get_player_type(self) -> str:
        """
        Get the type pf player (string), returns one of:
            - An immortal type:
                * One of settings.IMMORTAL_LEVELS tuple text values.
            - Dead
            - Survival
            - Classic
        """
        if self.is_immortal:
            return self.immortal_type

        if self.is_deleted == 1:
            return "Dead"

        if self.is_survival:
            return "Survival"

        return "Classic"

    @property
    @admin.display(boolean=False, description="Type")
    def player_type(self) -> str:
        """
        Player type.
        """
        return self.get_player_type()

    @property
    def podir(self) -> str:
        """
        Player "Podir" folder on disk.
        """
        return f'{settings.MUD_PODIR}/{self.name}'

    @property
    @admin.display(description="Seasonal Earned", ordering="seasonal_earned")
    def seasonal_earned(self) -> int:
        """
        Amount of essence earned for the player.
        """

        # Immortal players do not earn essence
        if self.is_immortal:
            return 0

        # Survival players earn less essence from renown
        divisor = 10
        if self.is_survival:
            divisor = 20

        # Start with two (2) points for existing,
        #   with renown/remort equation
        earned = int(self.total_renown / divisor) + 2
        if self.remorts > 0:
            earned += int(self.remorts / 5) * 3 + 1
        return earned
