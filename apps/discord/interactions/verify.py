"""Verify Ed25519 signatures on incoming Discord interaction requests."""

from django.conf import settings
from django.http import HttpRequest
from nacl.signing import VerifyKey


def verify(request: HttpRequest) -> None:
    """Verify the signature on an incoming Discord HTTPS request.

    Raises ``ValueError`` if required headers are missing.
    Raises ``nacl.exceptions.BadSignatureError`` if verification fails.
    """
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    body = request.body.decode("utf-8")

    if not signature or not timestamp or not body:
        raise ValueError("Missing Discord request header signature data.")

    verify_key = VerifyKey(bytes.fromhex(settings.DISCORD["PUBLIC_KEY"]))
    verify_key.verify(
        f"{timestamp}{body}".encode(),
        bytes.fromhex(signature),
    )
