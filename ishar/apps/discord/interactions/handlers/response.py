from django.http import JsonResponse


def respond(message=None, msg_type=4, status=200) -> JsonResponse:
    """Build and return a JSON response."""

    # Set response message type, and content, with HTTP code/status.
    response_data = {"type": msg_type, "data": {"content": message}}
    return JsonResponse(data=response_data, status=status)
