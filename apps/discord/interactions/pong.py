from django.http import JsonResponse

from .log import logger


def pong() -> JsonResponse:
    """Reply to ping, with pong, for URL validation."""
    logger.info("PING OK.")
    return JsonResponse({"type": 1})
