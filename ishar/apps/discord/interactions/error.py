from django.http import JsonResponse

from .log import logger


def error(message="Invalid request.", status=400) -> JsonResponse:
    """Log any errors, and return them as JSON."""
    logger.error("%s (%s)" % (message, status))
    return JsonResponse(data={"error": message}, status=status)
