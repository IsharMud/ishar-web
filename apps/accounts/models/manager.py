import secrets
from datetime import datetime, timezone

from django.contrib.auth.models import BaseUserManager
from django.db import IntegrityError
from django.utils.timezone import now
from passlib.hash import md5_crypt

from apps.accounts.validators import CROCKFORD32
from apps.core.utils.ip import ip2dec

# accounts.account_gift is a NOT NULL TIMESTAMP the game seeds with
# FROM_UNIXTIME(0); epoch+1s stays inside the TIMESTAMP range under strict
# SQL mode.
ACCOUNT_GIFT_NEVER = datetime(1970, 1, 1, 0, 0, 1, tzinfo=timezone.utc)


def gen_friend_code() -> str:
    # The game's algorithm (src/kernel/accounts.c): 5 random bytes packed
    # into 40 bits, emitted as 8 Crockford-base32 characters.
    packed = int.from_bytes(secrets.token_bytes(5), "big")
    out = []
    for _ in range(8):
        out.append(CROCKFORD32[packed & 0x1F])
        packed >>= 5
    return "".join(reversed(out))


class AccountManager(BaseUserManager):
    """Ishar account manager."""

    def create_user(
        self, email=None, account_name=None, password=None,
        ip=None, ident="web", referrer=None,
    ):
        """Insert an ``accounts`` row the way the game does.

        The table is the game's (``managed = False``): every NOT NULL
        column without a usable database default is set explicitly, the
        password is the game's MD5-crypt scheme, and a duplicate key is an
        error — never an upsert (ishar-mud#1711). ``ident`` marks the
        row's origin (game rows carry the socket's identd string).
        """
        if not email:
            raise ValueError("E-mail address is required.")
        if not account_name:
            raise ValueError("Account name is required.")
        if not password:
            raise ValueError("Password is required.")

        # The game stores only the /16 of the creating address as its ISP
        # (get_dotted_quad(haddr & 0xffff0000)).
        haddr = ip2dec(ip)
        isp = ".".join(ip.split(".")[:2] + ["0", "0"]) if ip else ""
        when = now()

        # friend_code is NOT NULL UNIQUE: a 40-bit collision is unlikely
        # but survivable — regenerate and retry. Any other duplicate key
        # (email/name race) re-raises for the caller to surface.
        for attempt in range(5):
            try:
                return self.create(
                    email=self.normalize_email(email),
                    account_name=account_name.lower(),
                    password=md5_crypt.hash(secret=password),
                    created_at=when,
                    current_essence=0,
                    earned_essence=0,
                    bugs_reported=0,
                    account_gift=ACCOUNT_GIFT_NEVER,
                    banned_until=None,
                    create_isp=isp,
                    last_isp=isp,
                    create_ident=ident,
                    last_ident=ident,
                    create_haddr=haddr,
                    last_haddr=haddr,
                    immortal_level=0,
                    is_private=False,
                    comm=0,
                    achievement_points=0,
                    beta_tester=0,
                    free_refresh=0,
                    friend_code=gen_friend_code(),
                    referrer_account=referrer,
                    email_verified_at=when,
                )
            except IntegrityError as exc:
                if attempt < 4 and "friend_code" in str(exc):
                    continue
                raise

    def create_superuser(self, email=None, account_name=None, password=None):
        user = self.create_user(
            email=email,
            account_name=account_name,
            password=password,
        )
        user.immortal_level = 5
        user.save()
        return user

    def get_by_natural_key(self, account_name):
        # Natural key of the account username.
        return self.get(account_name=account_name)
