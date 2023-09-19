from datetime import timedelta

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from ..accounts.models import Account
from ..classes.models import Class
from ..races.models import Race
from ..skills.models import Skill

from ...util.ip import dec2ip
from ...util.level import get_immortal_level, get_immortal_type


class PlayerFlag(models.Model):
    """
    Player Flag.
    """
    flag_id = models.AutoField(
        db_column="flag_id",
        primary_key=True,
        help_text="Auto-generated permanent player flag identification number.",
        verbose_name="Player Flag ID"
    )
    name = models.CharField(
        blank=False,
        db_column="name",
        max_length=20,
        null=False,
        help_text="Name of the player flag.",
        unique=True,
        verbose_name="Player Flag Name"
    )

    class Meta:
        managed = False
        db_table = "player_flags"
        ordering = ("name", "flag_id")
        verbose_name = "Flag"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {repr(self.__str__())} ({self.flag_id})"
        )

    def __str__(self) -> str:
        return self.name


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
    id = models.AutoField(
        blank=False,
        null=False,
        primary_key=True,
        help_text="Auto-generated permanent player identification number.",
        unique=True,
        verbose_name="ID"
    )
    name = models.SlugField(
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
        ordering = ("id",)
        verbose_name = "Player"

    def __repr__(self) -> str:
        return (
            f"Player: {repr(self.__str__())} ({self.id}) "
            f"[{self.get_player_type()}]"
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

    @admin.display(boolean=True, description="Forger?", ordering="-true_level")
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
        if self.common.level >= get_immortal_level(immortal_type=immortal_type):
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
    def player_css(self):
        """
        Player CSS class.
        """
        return f"{self.get_player_type().lower()}-player"

    @property
    def player_stats(self) -> dict:
        """
        Player stats.
        """

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
            "Willpower": self.common.willpower
        }

        # Put players stats in appropriate order, based on their class.
        stats_order = settings.CLASS_STATS.get(None)
        class_name = self.common.player_class.class_name
        if class_name in settings.CLASS_STATS:
            stats_order = settings.CLASS_STATS.get(class_name)

        for stat_order in stats_order:
            stats[stat_order] = players_stats[stat_order]

        return stats

    def get_immortal_type(self) -> (str, None):
        """
        Type of immortal.
        Returns one of settings.IMMORTAL_LEVELS tuple text values,
            from settings.IMMORTAL_LEVELS, or None.
        """
        return get_immortal_type(level=self.true_level)

    def get_player_alignment(self) -> str:
        """
        Player alignment.
        """
        for align_text, (low, high) in settings.ALIGNMENTS.items():
            if low <= self.common.alignment <= high:
                return align_text
        return "Unknown"

    def get_player_phrase(self) -> str:
        """
        Player phrase.
        """
        if self.is_deleted is True:
            return "was"
        return "is"

    def get_player_phrase_own(self) -> str:
        """
        Player phrase for ownership.
        """
        if self.is_deleted is True:
            return "were"
        return "are"

    def get_player_phrase_owns(self) -> str:
        """
        Player phrase for plural ownership.
        """
        if self.is_deleted is True:
            return "had"
        return "has"

    def get_player_gender(self) -> str:
            """
            Player gender.
            """
            if self.common.get_sex_display() == "Male":
                return "he"

            if self.common.get_sex_display() == "Female":
                return "she"

            return "they"

    def get_player_gender_own(self) -> str:
        """
        Player gender ownership.
        """
        if self.common.get_sex_display() == "Male":
            return "his"

        if self.common.get_sex_display() == "Female":
            return "her"

        return "their"

    def get_player_gender_owns(self) -> str:
        """
        Player gender ownership plural.
        """
        if self.common.get_sex_display() == "Male":
            return "his"

        if self.common.get_sex_display() == "Female":
            return "hers"

        return "have"

    def get_player_type(self):
        """
        Get the type pf player (string), returns one of:
            - Dead
            - An immortal type:
                * One of settings.IMMORTAL_LEVELS tuple text values.
            - Survival
            - Classic
        """
        if self.is_deleted == 1:
            return "Dead"

        if self.true_level >= min(settings.IMMORTAL_LEVELS)[0]:
            return get_immortal_type(level=self.true_level)

        if self.is_survival() is True:
            return "Survival"

        return "Classic"

    @admin.display(boolean=False, description="Online Time")
    def online_time(self) -> timedelta:
        """
        Online time.
        """
        return timedelta(seconds=self.online)

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
        if self.is_immortal() is True:
            return 0

        # Survival players earn less essence from renown
        divisor = 10
        if self.is_survival() is True:
            divisor = 20

        # Start with two (2) points for existing,
        #   with renown/remort equation
        earned = int(self.total_renown / divisor) + 2
        if self.remorts > 0:
            earned += int(self.remorts / 5) * 3 + 1
        return earned


class RemortUpgrade(models.Model):
    """
    Remort Upgrade.
    """
    upgrade_id = models.PositiveIntegerField(
        help_text=(
            "Auto-generated, permanent identification number of the "
            "remort upgrade."
        ),
        primary_key=True,
        verbose_name="Upgrade ID"
    )
    name = models.CharField(
        help_text="Name of the remort upgrade.",
        max_length=20,
        unique=True,
        verbose_name="Name"
    )
    renown_cost = models.PositiveSmallIntegerField(
        help_text="Renown cost of the remort upgrade.",
        verbose_name="Renown Cost"
    )
    max_value = models.PositiveSmallIntegerField(
        help_text="Maximum value of the remort upgrade.",
        verbose_name="Maximum Value"
    )
    scale = models.IntegerField(
        help_text="Scale of the remort upgrade.",
        verbose_name="Scale"
    )
    display_name = models.CharField(
        help_text="Display name of the remort upgrade.",
        max_length=30,
        verbose_name="Display Name"
    )
    can_buy = models.BooleanField(
        help_text="Whether the remort upgrade can be bought.",
        verbose_name="Can Buy?"
    )
    bonus = models.IntegerField(
        help_text="Bonus of the remort upgrade.",
        verbose_name="Bonus"
    )
    survival_scale = models.IntegerField(
        help_text="Scale of the remort upgrade, for survival players.",
        verbose_name="Survival Scale"
    )
    survival_renown_cost = models.IntegerField(
        help_text="Renown cost of the remort upgrade, for survival players.",
        verbose_name="Survival Renown Cost"
    )

    class Meta:
        db_table = "remort_upgrades"
        managed = False
        ordering = ("-can_buy", "display_name",)
        verbose_name = "Remort Upgrade"

    def __repr__(self):
        return f"{self.__class__.__name__}: {repr(self.__str__())}"

    def __str__(self):
        return self.display_name


class PlayerCommon(models.Model):
    """
    Player common attributes for class, race, level, etc.
    """
    player = models.OneToOneField(
        db_column="player_id",
        help_text="Player character with common attributes.",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="common",
        related_query_name="common",
        to=Player,
        to_field="id",
        verbose_name="Player"
    )
    player_class = models.ForeignKey(
        db_column="class_id",
        help_text="Class of the player character.",
        on_delete=models.CASCADE,
        related_query_name="+",
        to=Class,
        verbose_name="Class"
    )
    race = models.ForeignKey(
        db_column="race_id",
        help_text="Race of the player character.",
        on_delete=models.CASCADE,
        related_query_name="+",
        to=Race,
        verbose_name="Race"
    )
    sex = models.IntegerField(
        choices=settings.PLAYER_GENDERS,
        help_text="Sex of the player character.",
        verbose_name="Sex"
    )
    level = models.PositiveIntegerField(
        help_text="Level of the player character.",
        verbose_name="Level"
    )
    weight = models.PositiveSmallIntegerField(
        help_text="Weight of the player character.",
        verbose_name="Weight"
    )
    height = models.PositiveSmallIntegerField(
        help_text="Height of the player character.",
        verbose_name="Height"
    )
    comm_points = models.SmallIntegerField(
        help_text="Communication points of the player character.",
        verbose_name="Communication Points"
    )
    alignment = models.SmallIntegerField(
        help_text="Alignment of the player character.",
        verbose_name="Alignment"
    )
    strength = models.PositiveIntegerField(
        help_text="Strength of the player character.",
        verbose_name="Strength"
    )
    agility = models.PositiveIntegerField(
        help_text="Agility of the player character.",
        verbose_name="Agility"
    )
    endurance = models.PositiveIntegerField(
        help_text="Endurance of the player character.",
        verbose_name="Endurance"
    )
    perception = models.PositiveIntegerField(
        help_text="Perception of the player character.",
        verbose_name="Perception"
    )
    focus = models.PositiveIntegerField(
        help_text="Focus of the player character.",
        verbose_name="Focus"
    )
    willpower = models.PositiveIntegerField(
        help_text="Willpower of the player character.",
        verbose_name="Willpower"
    )
    init_strength = models.PositiveIntegerField(
        help_text="Initial strength of the player character.",
        verbose_name="Initial Strength"
    )
    init_agility = models.PositiveIntegerField(
        help_text="Initial agility of the player character.",
        verbose_name="Initial Agility"
    )
    init_endurance = models.PositiveIntegerField(
        help_text="Initial endurance of the player character.",
        verbose_name="Initial Endurance"
    )
    init_perception = models.PositiveIntegerField(
        help_text="Initial perception of the player character.",
        verbose_name="Initial Perception"
    )
    init_focus = models.PositiveIntegerField(
        help_text="Initial focus of the player character.",
        verbose_name="Initial Focus"
    )
    init_willpower = models.PositiveIntegerField(
        help_text="Initial willpower of the player character.",
        verbose_name="Initial Willpower"
    )
    perm_hit_pts = models.SmallIntegerField(
        help_text="Permanent hit points of the player character.",
        verbose_name="Permanent Hit Points"
    )
    perm_move_pts = models.SmallIntegerField(
        help_text="Permanent movement points of the player character.",
        verbose_name="Permanent Movement Points"
    )
    perm_spell_pts = models.SmallIntegerField(
        help_text="Permanent spell points of the player character.",
        verbose_name="Permanent Spell Points"
    )
    perm_favor_pts = models.SmallIntegerField(
        help_text="Permanent favor points of the player character.",
        verbose_name="Permanent Favor Points"
    )
    curr_hit_pts = models.SmallIntegerField(
        help_text="Current hit points of the player character.",
        verbose_name="Current Hit Points"
    )
    curr_move_pts = models.SmallIntegerField(
        help_text="Current movement points of the player character.",
        verbose_name="Current Movement Points"
    )
    curr_spell_pts = models.SmallIntegerField(
        help_text="Current spell points of the player character.",
        verbose_name="Current Spell Points"
    )
    curr_favor_pts = models.SmallIntegerField(
        help_text="Current favor points of the player character.",
        verbose_name="Current Favor Points"
    )
    experience = models.IntegerField(
        help_text="Experience points for the player character.",
        verbose_name="Experience"
    )
    gold = models.IntegerField(
        help_text="Value of gold that the player character has.",
        verbose_name="Gold"
    )
    karma = models.IntegerField(
        help_text="Karma value for the player character.",
        verbose_name="Karma"
    )

    class Meta:
        managed = False
        db_table = "player_common"
        default_related_name = "common"
        ordering = ("player_id",)
        verbose_name = "Player Common"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {repr(self.__str__())} ({self.id})"
        )

    def __str__(self) -> str:
        return self.player.name


class PlayersFlag(models.Model):
    """
    Player's Flag.
    """
    flag = models.ForeignKey(
        to=PlayerFlag,
        on_delete=models.CASCADE,
        related_query_name="+",
        help_text="Flag affecting a player.",
        verbose_name="Flag"
    )
    player = models.ForeignKey(
        to=Player,
        on_delete=models.CASCADE,
        related_name="flag",
        related_query_name="flags",
        help_text="Player affected by a flag.",
        verbose_name="Player"
    )
    value = models.PositiveIntegerField(
        blank=False,
        default=0,
        null=True,
        help_text="Value of the flag affecting the player.",
        verbose_name="Value"
    )

    class Meta:
        managed = False
        db_table = "player_player_flags"
        # The composite primary key (flag_id, player_id) found,
        #   that is not supported. The first column is selected.
        unique_together = (("flag", "player"),)
        ordering = ("flag", "player")
        verbose_name = "Player's Flag"
        verbose_name_plural = "Player's Flags"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {repr(self.__str__())}"
        )

    def __str__(self) -> str:
        return f"{self.flag} @ {self.player} : {self.value}"


class PlayerRemortUpgrade(models.Model):
    """
    Player Remort Upgrade.
    """
    upgrade = models.ForeignKey(
        db_column="upgrade_id",
        related_query_name="+",
        to=RemortUpgrade,
        to_field="upgrade_id",
        on_delete=models.CASCADE,
        help_text="Remort upgrade affecting a player.",
        verbose_name="Remort Upgrade"
    )
    player = models.ForeignKey(
        db_column="player_id",
        related_query_name="upgrade",
        related_name="upgrades",
        to=Player,
        to_field="id",
        on_delete=models.CASCADE,
        help_text="Player with a remort upgrade.",
        verbose_name="Player"
    )
    value = models.PositiveIntegerField(
        blank=False,
        default=0,
        null=False,
        help_text="Value of a player's remort upgrade.",
        verbose_name="Value"
    )
    essence_perk = models.BooleanField(
        help_text="Is the player's remort upgrade an essence perk?",
        verbose_name="Essence Perk?"
    )

    class Meta:
        managed = False
        db_table = "player_remort_upgrades"
        unique_together = (("upgrade", "player"),)
        ordering = ("upgrade", "player")
        verbose_name = "Player Remort Upgrade"
        verbose_name_plural = "Player Remort Upgrades"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {repr(self.__str__())}"
        )

    def __str__(self) -> str:
        return f"{self.upgrade} @ {self.player} : {self.value}"


class PlayerSkill(models.Model):
    """
    Player Skill.
    """
    skill = models.ForeignKey(
        db_column="skill_id",
        related_query_name="+",
        to=Skill,
        to_field="id",
        on_delete=models.CASCADE,
        help_text="Skill/spell related to a player.",
        verbose_name="Skill"
    )
    player = models.ForeignKey(
        db_column="player_id",
        related_query_name="skill",
        related_name="skills",
        to=Player,
        to_field="id",
        on_delete=models.CASCADE,
        help_text="Player with a skill/spell.",
        verbose_name="Player"
    )
    skill_level = models.PositiveIntegerField(
        help_text="Skill level of the player's skill.",
        verbose_name="Skill Level"
    )

    class Meta:
        managed = False
        db_table = "player_skills"
        # The composite primary key (skill_id, player_id) found,
        #   that is not supported. The first column is selected.
        unique_together = (("skill", "player"),)
        ordering = ("skill", "player")
        verbose_name = "Player Skill"
        verbose_name_plural = "Player Skills"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {repr(self.__str__())}"
        )

    def __str__(self) -> str:
        return f"{self.skill} @ {self.player} : {self.skill_level}"
