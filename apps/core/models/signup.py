"""Pending e-mail verifications for web signup.

Verify-first: no ``accounts`` row exists until the e-mailed code is
confirmed, so the game's table never holds unverified signups. One live
verification per e-mail (a resend refreshes the row). Site-owned table,
same ``managed = True`` pattern as ``web_hud_bar``; codes are stored
hashed. Lives in core (not accounts) because the accounts app must stay
migration-free — applied migrations elsewhere already carry
``swappable_dependency(AUTH_USER_MODEL)``, and a first accounts migration
would make that history inconsistent on every existing database.
"""
import hashlib

from django.db import models

from .unsigned import UnsignedAutoField


class SignupVerification(models.Model):
    """One pending signup: an e-mail address and its hashed code."""

    CODE_TTL_SECONDS = 15 * 60
    MAX_ATTEMPTS = 5
    MAX_SENDS = 5
    RESEND_COOLDOWN_SECONDS = 60

    id = UnsignedAutoField(primary_key=True)
    email = models.EmailField(
        unique=True,
        max_length=30,
        help_text="E-mail address being verified.",
        verbose_name="E-mail Address",
    )
    code_hash = models.CharField(
        max_length=64,
        help_text="SHA-256 of 'email:code'; the code itself is never stored.",
        verbose_name="Code Hash",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )
    expires_at = models.DateTimeField(
        help_text="Codes are valid for 15 minutes from the last send.",
        verbose_name="Expires At",
    )
    attempts = models.PositiveSmallIntegerField(
        default=0,
        help_text="Wrong-code attempts; the row is deleted at the cap.",
        verbose_name="Attempts",
    )
    send_count = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Send Count",
    )
    last_sent_at = models.DateTimeField(
        verbose_name="Last Sent At",
    )

    class Meta:
        managed = True
        db_table = "web_signup_verification"
        verbose_name = "Signup Verification"
        verbose_name_plural = "Signup Verifications"

    def __str__(self) -> str:
        return f"Signup verification for {self.email}"

    @staticmethod
    def hash_code(email: str, code: str) -> str:
        payload = f"{email.lower()}:{code}".encode()
        return hashlib.sha256(payload).hexdigest()

    def matches(self, code: str) -> bool:
        return self.code_hash == self.hash_code(self.email, code)
