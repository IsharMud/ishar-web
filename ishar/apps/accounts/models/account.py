from datetime import datetime
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from libgravatar import Gravatar, sanitize_email
from passlib.hash import md5_crypt

from ishar.apps.core.utils.ip import dec2ip

from .level import ImmortalLevel
from .manager import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    """Ishar user account that logs in to the website, and MUD/game."""

    account_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated permanent unique account number.",
        verbose_name="Account ID"
    )
    created_at = models.DateTimeField(
        help_text="Date and time when the account was created.",
        verbose_name="Created At"
    )
    current_essence = models.PositiveIntegerField(
        help_text="Current amount of essence for the account.",
        verbose_name="Current Essence"
    )
    email = models.EmailField(
        unique=True,
        max_length=30,
        help_text="E-mail address for the account.",
        verbose_name="E-mail Address"
    )
    password = models.CharField(
        max_length=36,
        help_text="Account password (MD5Crypt) hash.",
        verbose_name="Password"
    )
    create_isp = models.CharField(
        max_length=25,
        help_text="Internet Service Provider (ISP) that created the account.",
        verbose_name="Create ISP"
    )
    last_isp = models.CharField(
        max_length=25,
        help_text=(
            "Last Internet Service Provider (ISP) that logged in to the "
            "account."
        ),
        verbose_name="Last ISP"
    )
    create_ident = models.CharField(
        max_length=25,
        help_text="Ident that created the account.",
        verbose_name="Create IDENT"
    )
    last_ident = models.CharField(
        max_length=25,
        help_text="Last ident that logged in to the account.",
        verbose_name="Last IDENT"
    )
    create_haddr = models.IntegerField(
        help_text="HADDR that created the account.",
        verbose_name="Create HADDR"
    )
    last_haddr = models.IntegerField(
        help_text="Last HADDR to log in to the account.",
        verbose_name="Last HADDR"
    )
    account_name = models.SlugField(
        unique=True,
        max_length=25,
        help_text="User-chosen account name for logging in.",
        verbose_name="Account Name"
    )
    account_gift = models.DateTimeField(
        help_text="Date and time of account gift.",
        verbose_name="Account Gift"
    )
    banned_until = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date and time account is banned until.",
        verbose_name="Banned Until"
    )
    bugs_reported = models.IntegerField(
        help_text="Number of bugs reported.",
        verbose_name="Bugs Reported"
    )
    earned_essence = models.IntegerField(
        help_text="Amount of essence earned.",
        verbose_name="Earned Essence"
    )
    immortal_level = models.SmallIntegerField(
        blank=True,
        choices=ImmortalLevel,
        null=True,
        help_text="Immortal level of the account.",
        verbose_name="Immortal Level"
    )
    is_private = models.BooleanField(
        db_column="is_private",
        default=False,
        help_text="Does the account want private player profiles?",
        verbose_name="Is Private?"
    )
    comm = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of communication points for the communication.",
        verbose_name="Communication Points"
    )
    achievement_points = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Number of achievement points for the account.",
        verbose_name="Achievement Points"
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "account_name"
    objects = AccountManager()
    user_permissions = None

    class Meta:
        db_table = "accounts"
        default_related_name = "account"
        managed = False
        ordering = ("account_id",)
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return self.get_username()

    def check_password(self, raw_password: str = None) -> bool:
        """Check account password."""
        return md5_crypt.verify(secret=raw_password, hash=self.password)

    @property
    @admin.display(description="Create IP", ordering="create_haddr")
    def create_ip(self) -> (str, None):
        """IP address that created the account."""
        return dec2ip(self.create_haddr)

    @property
    @admin.display(description="Last IP", ordering="last_haddr")
    def last_ip(self) -> (str, None):
        """IP address that last logged into the account."""
        return dec2ip(self.last_haddr)

    def get_gravatar(self) -> (str, None):
        """Gravatar.com image for any account e-mail address."""
        if self.email and "@" in self.email:
            email = sanitize_email(self.email)
            avatar = Gravatar(email)
            if avatar:
                image = avatar.get_image()
                if image:
                    return image
        return None

    def get_username(self) -> str:
        """Return account username."""
        return getattr(self, self.USERNAME_FIELD)

    def has_perms(self, perm_list, obj=None) -> bool:
        return self.is_god()

    def has_module_perms(self, app_label) -> bool:
        return self.is_god()

    @property
    @admin.display(boolean=True, description="Active?")
    def is_active(self) -> bool:
        """Boolean whether account is active."""
        if self.is_banned() is True:
            return False
        return True

    @admin.display(boolean=True, description="Banned?")
    def is_banned(self) -> bool:
        if self.banned_until and isinstance(self.is_banned, datetime):
            if self.banned_until > timezone.now():
                return True
        return False

    @admin.display(boolean=True, description="Artisan?")
    def is_artisan(self) -> bool:
        """Boolean whether Artisan (or above)."""
        if self.immortal_level:
            if self.immortal_level >= ImmortalLevel.ARTISAN:
                return True
        return False

    @admin.display(boolean=True, description="Eternal?")
    def is_eternal(self) -> bool:
        """Boolean whether Eternal (or above)."""
        if self.immortal_level:
            if self.immortal_level >= ImmortalLevel.ETERNAL:
                return True
        return False

    @admin.display(boolean=True, description="Forger?")
    def is_forger(self) -> bool:
        """Boolean whether Forger (or above)."""
        if self.immortal_level:
            if self.immortal_level >= ImmortalLevel.FORGER:
                return True
        return False

    @admin.display(boolean=True, description="God?")
    def is_god(self) -> bool:
        """Boolean whether God (or above?)."""
        if self.immortal_level:
            if self.immortal_level >= ImmortalLevel.GOD:
                return True
        return False

    @admin.display(boolean=True, description="Immortal?")
    def is_immortal(self) -> bool:
        """Boolean whether immortal, or above."""
        if self.immortal_level:
            if self.immortal_level >= ImmortalLevel.IMMORTAL:
                return True
        return False

    # "God"s are administrators/superusers, for Django Admin.
    is_admin = is_superuser = is_god

    @property
    def is_staff(self) -> bool:
        """Eternals, and above, can log in to Django Admin."""
        if self.is_eternal() is True:
            return True
        return False

    @property
    def last_login(self) -> datetime:
        """Most recent login of all players for the account."""
        when = self.created_at
        for player in self.players.all():
            if player.logon < when:
                when = player.logon
        return when

    def natural_key(self) -> str:
        """Natural key of the account username."""
        return getattr(self, self.USERNAME_FIELD)

    @property
    @admin.display(description="# Players", ordering="player_count")
    def player_count(self) -> int:
        """Number of players for the account."""
        return self.players.count()

    @property
    def seasonal_earned(self) -> int:
        """Amount of essence earned for the account."""
        # Start at zero (0), and return the points from
        #   the player character within the account with the highest amount.
        earned = 0
        for player in self.players.all():
            if player.seasonal_earned > earned:
                earned = player.seasonal_earned
        return earned

    def set_password(self, raw_password: str = None) -> bool:
        """Method to set the account password."""
        self.password = md5_crypt.hash(secret=raw_password)
        if self.save():
            return True
        return False

    def upgrades(self) -> iter:
        """Method to find active account upgrades for the account."""
        return self.all_upgrades.filter(
            account=self,
            amount__gt=0
        )
