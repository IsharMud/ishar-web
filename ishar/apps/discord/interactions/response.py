from django.http import JsonResponse

from .error import error


def respond(message=None, msg_type=4, status=200) -> JsonResponse:
    """Build and return a JSON response."""

    if message is not None:

        # Set the message type, and data/content, as well as its HTTP status.
        return JsonResponse(
            data={
                "type": msg_type,
                "data": {
                    "content": message
                }
            },
            status=status
        )

    # Last resort is to return an error.
    return error()
