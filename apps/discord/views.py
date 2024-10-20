from json import loads as json_loads
from logging import getLogger

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from nacl.exceptions import BadSignatureError

from apps.core.views.mixins import NeverCacheMixin

from .interactions.handlers.slash import slash
from .interactions.verify import verify


logger = getLogger(__name__)


class InteractionsView(NeverCacheMixin, View):
    """Interactions view."""
    http_method_names = ("post",)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        # Disable CSRF protection for inbound Discord requests.
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs) -> JsonResponse:
        # Handle incoming POST requests (slash commands).

        # Verify signature sent in the HTTPS request headers from Discord.
        try:
            verified = verify(request)

            if verified is not True:
                return JsonResponse(
                    data={"error": "Cannot verify signature."},
                    status=500
                )

        except BadSignatureError as discord_bad_sig:
            logger.exception(discord_bad_sig)
            return JsonResponse(
                data={"error": "Invalid signature!"},
                status=401
            )

        except ValueError as discord_sig_missing:
            logger.exception(discord_sig_missing)
            return JsonResponse(
                data={"error": "Missing signature."},
                status=400
            )

        # Decode JSON of the interaction, and get interaction type.
        interaction = {"body": request.body.decode("utf-8")}
        interaction["json"] = json_loads(interaction["body"])
        interaction["type"] = interaction["json"].get("type")

        # Ping/pong.
        if interaction["type"] == 1:
            return JsonResponse(data={"type": 1}, status=200)

        # Slash (/) commands.
        if interaction["type"] == 2:
            ephemeral = True  # Respond to only the user, by default.
            try:
                message, ephemeral = slash(
                    interaction_json=interaction["json"],
                    request=request
                )

            # Handle unknown slash commands.
            except ModuleNotFoundError as unknown_slash:
                logger.exception(unknown_slash)
                message = "Unknown command."
                ephemeral = True

            # Finally, build the reply to the slash command.
            response = {
                "data": {
                    "content": message
                },
                "type": 4
            }

            # Mark the message ephemeral, when necessary.
            if ephemeral is True:
                response["data"]["flags"] = 64

            return JsonResponse(data=response, status=200)

        # Unknown interaction type.
        logger.error(f"Unknown Discord interaction:\n{interaction}")
        return JsonResponse(data={"error": "Unknown interaction."}, status=401)
