from datetime import timedelta
from pathlib import Path

from django.db import models
from django.conf import settings
from django.contrib.admin import display
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.html import format_html
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Account
from apps.core.models.title import Title
from apps.core.utils.ip import dec2ip

from .game_type import GameType
from ..utils import get_immortal_level, get_immortal_type


class PlayerBaseManager(models.Manager):
    def get_by_natural_key(self, name):
        # Natural key is player name.
        return self.get(name=name)


class PlayerBase(models.Model):
    """Ishar player base model."""

    objects = PlayerBaseManager()

    account = models.ForeignKey(
        to=Account,
        on_delete=models.DO_NOTHING,
        related_query_name="player",
        related_name="players",
        help_text="Account that owns the player character.",
        verbose_name="Account",
    )
    id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated permanent player identification number.",
        verbose_name="(Player) ID",
    )
    name = models.SlugField(
        unique=True,
        max_length=15,
        help_text="Name of the player character.",
        verbose_name="Name",
    )
    create_ident = models.CharField(
        max_length=10,
        help_text="Ident that created the player.",
        verbose_name="Create IDENT",
    )
    last_isp = models.CharField(
        max_length=30,
        help_text="Last Internet Service Provider (ISP) to join as the player.",
        verbose_name="Create IDENT",
    )
    description = models.CharField(
        max_length=240,
        blank=True,
        null=True,
        help_text="User-written in-game player description.",
        verbose_name="Description",
    )
    title = models.CharField(
        db_column="title",
        max_length=45,
        help_text="User-selectable player title.",
        verbose_name="Title",
    )
    title_id = models.ForeignKey(
        blank=True,
        db_column="title_id",
        null=True,
        to=Title,
        on_delete=models.DO_NOTHING,
        help_text=_("Title related to an account."),
        verbose_name=_("Title"),
    )
    poofin = models.CharField(
        max_length=80,
        help_text="String displayed upon player poof in.",
        verbose_name="Poof In",
    )
    poofout = models.CharField(
        max_length=80,
        help_text="String displayed upon player poof out.",
        verbose_name="Poof In",
    )
    bankacc = models.PositiveIntegerField(
        help_text="Bank account balance.",
        verbose_name="Bank Account",
    )
    logon_delay = models.PositiveSmallIntegerField(
        help_text="Delay when logging on.",
        verbose_name="Logon Delay",
    )
    true_level = models.PositiveIntegerField(
        help_text="True level of the player character.",
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=settings.MAX_IMMORTAL_LEVEL),
        ],
        verbose_name="True Level",
    )
    renown = models.PositiveIntegerField(
        help_text="Amount of renown available for the player to spend.",
        verbose_name="Renown",
    )
    remorts = models.PositiveIntegerField(
        help_text="Number of times that the player has remorted.",
        verbose_name="Remorts",
    )
    favors = models.PositiveIntegerField(
        help_text="Amount of favors for the player.",
        verbose_name="Favors",
    )
    online = models.IntegerField(
        blank=True,
        null=True,
        help_text="Amount of time spent logged in to the game, in seconds.",
        verbose_name="Online",
    )
    bound_room = models.PositiveIntegerField(
        help_text="Room ID number where the player is bound.",
        verbose_name="Bound Room",
    )
    load_room = models.PositiveIntegerField(
        help_text="Room ID number where the player is loaded.",
        verbose_name="Load Room",
    )
    invstart_level = models.IntegerField(
        blank=True,
        null=True,
        help_text="Invisible Start Level.",
        verbose_name="Invisible Start Level",
    )
    login_failures = models.PositiveSmallIntegerField(
        help_text="Number of login failures.",
        verbose_name="Login Failures",
    )
    create_haddr = models.IntegerField(
        help_text="HADDR that created the player.",
        verbose_name="Create HADDR",
    )
    login_fail_haddr = models.IntegerField(
        blank=True,
        null=True,
        help_text="HADDR that last failed to log in to the player.",
        verbose_name="Login Fail HADDR",
    )
    last_haddr = models.IntegerField(
        blank=True,
        null=True,
        help_text="Last HADDR to join as the player.",
        verbose_name="Last HADDR",
    )
    last_ident = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Last ident to join as the player.",
        verbose_name="Last IDENT",
    )
    load_room_next = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Load Room Next.",
        verbose_name="Load Room Next",
    )
    load_room_next_expires = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Load Room Next Expires.",
        verbose_name="Load Room Next Expires",
    )
    aggro_until = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Aggro Until.",
        verbose_name="Aggro Until",
    )
    inn_limit = models.PositiveSmallIntegerField(
        help_text="Inn Limit.",
        verbose_name="Inn Limit",
    )
    held_xp = models.IntegerField(
        blank=True,
        null=True,
        help_text="Held XP.",
        verbose_name="Held XP",
    )
    last_isp_change = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Last Internet Service Provider (ISP) change.",
        verbose_name="Last ISP Change",
    )
    is_deleted = models.PositiveIntegerField(
        blank=False,
        default=0,
        null=False,
        help_text="Is the player character deleted?",
        verbose_name="Is Deleted?",
    )
    deaths = models.PositiveSmallIntegerField(
        help_text="Number of times that the player has died.",
        verbose_name="Deaths",
    )
    total_renown = models.PositiveSmallIntegerField(
        help_text="Total amount of renown earned by the player.",
        verbose_name="Total Renown",
    )
    quests_completed = models.PositiveSmallIntegerField(
        help_text="Total number of quests completed by the player.",
        verbose_name="Quests Completed",
    )
    challenges_completed = models.PositiveSmallIntegerField(
        help_text="Total number of challenges completed by the player.",
        verbose_name="Challenges Completed",
    )
    game_type = models.IntegerField(
        choices=GameType,
        help_text="Player game type.",
        verbose_name="Game Type",
    )
    birth = models.DateTimeField(
        help_text="Date and time that the player was created.",
        verbose_name="Birth",
    )
    logon = models.DateTimeField(
        help_text="Date and time that the player last logged on.",
        verbose_name="Log On",
    )
    logout = models.DateTimeField(
        help_text="Date and time that the player last logged out.",
        verbose_name="Log Out",
    )

    class Meta:
        managed = False
        db_table = "players"
        default_related_name = "player"
        ordering = ("id",)
        verbose_name = "Player"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.name

    def natural_key(self) -> str:
        # Natural key is player name.
        return self.name

    @property
    @display(description="Create IP", ordering="create_haddr")
    def _create_haddr(self) -> str:
        # IP address that created the account.
        return dec2ip(self.create_haddr)

    @property
    @display(description="Login Fail IP", ordering="login_fail_haddr")
    def _login_fail_haddr(self) -> str:
        # Last IP address that failed to log in to the account.
        return dec2ip(self.login_fail_haddr)

    @property
    @display(description="Last IP", ordering="last_haddr")
    def _last_haddr(self) -> str:
        # Last IP address that logged in to the account.
        return dec2ip(self.last_haddr)

    def get_absolute_url(self) -> str:
        # URL to player page
        return reverse(
            viewname="player",
            kwargs={"name": self.name}
        ) + "#player"

    def get_immortal_type(self) -> (str, None):
        # Type of immortal.
        #   Returns one of settings.IMMORTAL_LEVELS tuple text values, from
        #    settings.IMMORTAL_LEVELS, or None.
        return get_immortal_type(level=self.true_level)

    def get_player_alignment(self) -> str:
        # Player alignment.
        for align_text, (low, high) in settings.ALIGNMENTS.items():
            if low <= self.common.alignment <= high:
                return align_text
        return "Unknown"

    def get_player_phrase(self) -> str:
        # Player phrase.
        if self.is_deleted > 0:
            return "was"
        return "is"

    def get_player_phrase_own(self) -> str:
        # Player phrase for ownership.
        if self.is_deleted > 0:
            return "were"
        return "are"

    def get_player_phrase_owns(self) -> str:
        # Player phrase for plural ownership.
        if self.is_deleted > 0:
            return "had"
        return "has"

    def get_player_gender(self) -> str:
        # Player gender.
        if self.common.get_sex_display() == "Male":
            return "he"

        if self.common.get_sex_display() == "Female":
            return "she"

        return "they"

    def get_player_gender_own(self) -> str:
        # Player gender ownership.
        if self.common.get_sex_display() == "Male":
            return "his"

        if self.common.get_sex_display() == "Female":
            return "her"

        return "their"

    def get_player_gender_owns(self) -> str:
        # Player gender ownership plural.
        if self.common.get_sex_display() == "Male":
            return "his"

        if self.common.get_sex_display() == "Female":
            return "hers"

        return "have"

    def get_player_type(self) -> str:
        # Get the type of player.
        if self.is_deleted > 0:
            return "Dead"

        if self.true_level >= settings.MIN_IMMORTAL_LEVEL:
            return get_immortal_type(level=self.true_level)

        if self.is_hardcore() is True:
            return "Hardcore"

        if self.is_survival() is True:
            return "Survival"

        return "Classic"

    @display(boolean=True, description="Consort?", ordering="-true_level")
    def is_consort(self) -> bool:
        # Boolean whether player is consort, or above.
        return self.is_immortal_type(immortal_type="Consort")

    @display(boolean=True, description="Eternal?", ordering="-true_level")
    def is_eternal(self) -> bool:
        # Boolean whether player is eternal, or above.
        return self.is_immortal_type(immortal_type="Eternal")

    @display(boolean=True, description="Forger?", ordering="-true_level")
    def is_forger(self) -> bool:
        # Boolean whether player is consort, or above.
        return self.is_immortal_type(immortal_type="Forger")

    @display(boolean=True, description="God?", ordering="-true_level")
    def is_god(self) -> bool:
        # Boolean whether player is a "God".
        return self.is_immortal_type(immortal_type="God")

    @display(boolean=True, description="Immortal?", ordering="-true_level")
    def is_immortal(self) -> bool:
        # Boolean whether player is immortal, or above, but not consort.
        return self.is_immortal_type(immortal_type="Immortal")

    def is_immortal_type(self, immortal_type="Immortal") -> bool:
        # Boolean whether player is an immortal of a certain type, or above.
        if self.common.level >= get_immortal_level(immortal_type=immortal_type):
            return True
        return False

    @display(boolean=True, description="Hardcore?", ordering="-game_type")
    def is_hardcore(self) -> bool:
        # Boolean whether player is "hardcore".
        if self.game_type == GameType.HARDCORE:
            return True
        return False

    @display(boolean=True, description="Survival?", ordering="-game_type")
    def is_survival(self) -> bool:
        # Boolean whether player is "survival".
        if self.game_type == GameType.SURVIVAL:
            return True
        return False

    @display(boolean=False, description="Online Timedelta")
    def online_timedelta(self) -> timedelta:
        # Online timedelta.
        return timedelta(seconds=self.online)

    @display(boolean=False, description="Online Time")
    def online_time(self) -> str:
        # Online time humanized string.
        if self.online > 60:
            return timesince(now() - self.online_timedelta())
        return "%i seconds" % self.online

    @property
    def player_css(self) -> str:
        # Player CSS class.
        return f"{self.get_player_type().lower()}-player"

    @property
    def player_link(self) -> str:

        # Private accounts show only styled name.
        if self.account.is_private is True or self.is_immortal():
            return format_html(
                '<span class="{}" title="{}">{}</span>',
                self.player_css,
                self.name,
                self.name,
            )

        # Otherwise, styled link to player profile.
        return format_html(
            '<a class="{}" href="{}" title="{}">{}</a>',
            self.player_css,
            self.get_absolute_url(),
            self.name,
            self.name,
        )

    @property
    def player_stats(self) -> dict:
        # Player statistics.

        # Start with empty dictionary.
        stats = {}

        # Immortals have no stats.
        if self.is_immortal() is True:
            return stats

        # No stats for mortal players below level five (5),
        #   with less than one (1) hour of play-time
        if self.true_level < 5 and self.online < 3600:
            return stats

        # Otherwise, get the players actual stats
        players_stats = {
            "Agility": self.common.agility,
            "Endurance": self.common.endurance,
            "Focus": self.common.focus,
            "Perception": self.common.perception,
            "Strength": self.common.strength,
            "Willpower": self.common.willpower,
        }

        # Put players stats in appropriate order, based on their class.
        stats_order = settings.CLASS_STATISTICS.get(None)
        class_name = self.common.player_class.class_name
        if class_name in settings.CLASS_STATISTICS:
            stats_order = settings.CLASS_STATISTICS.get(class_name)

        for stat_order in stats_order:
            stats[stat_order] = players_stats[stat_order]

        return stats

    @property
    @display(boolean=False, description="Total Statistics")
    def get_total_statistics_count(self) -> int:
        # Total number of player statistics.
        return sum(self.player_stats.values())

    @property
    @display(boolean=False, description="Title", ordering="title")
    def player_title(self):
        # Player title.
        return self.title % self.name

    @display(boolean=False, description="Type", ordering="game_type")
    def player_type(self) -> str:
        # Player type.
        return self.get_player_type()

    @property
    @display(description="Seasonal Earned", ordering="seasonal_earned")
    def seasonal_earned(self) -> int:
        # Amount of essence earned for the player.

        # Immortal players do not earn essence.
        if self.is_immortal() is True:
            return 0

        # Start with two (2) points for existing, with renown/remort equation.
        earned = int(self.total_renown / 100) + 2
        if self.remorts > 0:
            earned += int(self.remorts / 5) * 3 + 1
        return earned

    def upgrades(self):
        # Method to find active remort upgrades for the player.
        return self.all_remort_upgrades.filter(
            player=self,
            value__gt=0
        )
