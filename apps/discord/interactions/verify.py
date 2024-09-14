from logging import getLogger
from django.conf import settings

from nacl.signing import VerifyKey


logger = getLogger(__name__)


def verify(request):
    """Verify signature via headers of incoming Discord HTTPS requests."""

    # Use our Discord application public key.
    verify_key = VerifyKey(bytes.fromhex(settings.DISCORD["PUBLIC_KEY"]))

    # Get the signature and timestamp from the request header.
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")

    # Decode the incoming POST data/body.
    body = request.body.decode("utf-8")

    # Return None if any expected data is missing.
    if not signature or not timestamp or not body:
        raise ValueError("Missing Discord request header signature data.")

    # Verify signature of the incoming POST request message body.
    string = f"{timestamp}{body}".encode()
    if verify_key.verify(string, bytes.fromhex(signature)):
        return True

    # Return False as last resort.
    return False
