import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from .interactions.error import error
from .interactions.handlers import handle_command
from .interactions.log import logger
from .interactions.pong import pong
from .interactions.verify import verify


class InteractionsView(View):
    """
    Interactions view.
    """
    http_method_names = ("get", "post")

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        """Disable CSRF protection for inbound Discord requests."""
        return super().dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs) -> JsonResponse:
        """Return 405 'Method Not Allowed' JSON error for GET requests."""
        return error("Method not allowed.", status=405)

    def post(self, request, *args, **kwargs) -> JsonResponse:
        """Handle incoming POST requests."""

        # Ensure that the incoming request has a valid signature.
        verification = verify(request)
        if verification is None:
            return error("Missing signature.", status=400)
        if verification is False:
            return error("Invalid signature.", status=400)
        if verification is not True:
            return error("Signature could not be verified.", status=500)

        # Get the contents of the interaction, and its type.
        interaction_body = json.loads(request.body.decode("utf-8"))
        interaction_type = interaction_body.get("type")

        # Reply to ping, with pong, for URL endpoint validation.
        if interaction_type == 1:
            return pong()

        # Reply to slash commands.
        if interaction_type == 2:
            return handle_command(
                interaction_data=interaction_body.get("data"),
                request=request
            )

        # Log and return JSON error for unknown interaction types.
        logger.error("Type %d:\n%s" % (interaction_type, interaction_body))
        return error(message="Unknown interaction type", status=400)
