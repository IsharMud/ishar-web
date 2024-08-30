import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from .interactions.error import error
from .interactions.exceptions import UnknownCommandException
from .interactions.handlers.response import respond
from .interactions.handlers.slash import slash
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

    @staticmethod
    def get(self, *args, **kwargs) -> JsonResponse:
        """Return 405 'Method Not Allowed' JSON error for GET requests."""
        return error("Method not allowed.", status=405)

    @staticmethod
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

        # Decode JSON of the interaction, and get interaction type.
        interaction = {"body": request.body.decode("utf-8")}
        interaction["json"] = json.loads(interaction["body"])
        interaction["type"] = interaction["json"].get("type")

        # Reply to ping, with pong, for URL endpoint validation.
        if interaction["type"] == 1:
            return pong()

        # Handle slash commands.
        if interaction["type"] == 2:

            # Process the slash command.
            ephemeral = True
            try:
                message, ephemeral = slash(
                    interaction_json=interaction["json"],
                    request=request
                )

            # Log and reply for unknown slash commands.
            except UnknownCommandException:
                logger.error("Unknown slash command:\n%s" % interaction)
                message = "Unknown slash command."

            # Reply to the slash command.
            return respond(message=message, ephemeral=ephemeral)

        # Log and return JSON error for unknown interaction type.
        logger.error("Unknown interaction type:\n%s" % interaction)
        return error(message="Unknown interaction type.", status=400)
