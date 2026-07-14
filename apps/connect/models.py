"""Web auto-login tokens (isharmud/ishar-mud#1773, Contract 3).

``web_login_token`` lets a portal-authenticated player land in the game from
``/connect`` without retyping credentials. The table is owned by the game
(``managed = False`` — its migration lives in ``ishar-mud``); the website is
the writer, the game the consumer. Contract:
``ishar-mud/docs/web_bridge_contracts.md``.

The flow, and the two rules that make it safe:

* The **Channels consumer** — never the page, never browser JS — mints
  ``secrets.token_urlsafe(32)`` for the authenticated ``scope["user"]``,
  stores **only its SHA-256 hex** here, and writes ``webauth <token>`` into
  the telnet stream itself. The plaintext token never reaches the browser
  (no DOM, no JS, no localStorage) and never reaches this table.
* The game consumes the row with **one atomic guarded UPDATE** (single use +
  TTL together), so a token grants exactly one login within 90 seconds, for
  exactly the account it was minted for. Any failure degrades to the manual
  login prompt.
"""
import hashlib
import secrets

from django.db import connection, models

from apps.core.models.unsigned import UnsignedAutoField


# Token lifetime, matching the game-side consumer's guard
# (``expires_at > NOW()``) and the bridge contract ("mint + 90s").
TOKEN_TTL_SECONDS = 90


class WebLoginToken(models.Model):
    """A single-use, short-lived auto-login token (hash only)."""

    id = UnsignedAutoField(primary_key=True)
    token_hash = models.CharField(
        max_length=64,
        unique=True,
        help_text="SHA-256 hex of the token; the plaintext is never stored.",
        verbose_name="Token Hash",
    )
    account_id = models.IntegerField(
        db_column="account_id",
        help_text="Account the token was minted for.",
        verbose_name="Account ID",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the token was minted.",
        verbose_name="Created At",
    )
    expires_at = models.DateTimeField(
        help_text="Mint time + 90 seconds; the game refuses the token after.",
        verbose_name="Expires At",
    )
    used_at = models.DateTimeField(
        null=True,
        help_text="When the game consumed the token (single use).",
        verbose_name="Used At",
    )

    class Meta:
        managed = False
        db_table = "web_login_token"
        verbose_name = "Web Login Token"
        verbose_name_plural = "Web Login Tokens"

    def __str__(self) -> str:
        return f"Web login token for account {self.account_id}"

    @classmethod
    def mint(cls, account_id: int) -> str:
        """Mint a token for *account_id* and return the plaintext.

        The row stores only the SHA-256; ``expires_at`` is computed **in the
        database** (``NOW() + INTERVAL 90 SECOND``) so the same clock that
        checks the TTL game-side also sets it — no Django/MariaDB timezone or
        clock-skew coupling. Raises on any DB error (e.g. the game migration
        has not run yet); the caller degrades to manual login.
        """
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode("ascii")).hexdigest()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO web_login_token (token_hash, account_id, expires_at)"
                " VALUES (%s, %s, NOW() + INTERVAL %s SECOND)",
                [token_hash, account_id, TOKEN_TTL_SECONDS],
            )
        return token
