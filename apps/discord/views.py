import json
from logging import getLogger

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from nacl.exceptions import BadSignatureError

from apps.core.views.mixins import NeverCacheMixin

from .interactions.handlers.slash import slash
from .interactions.verify import verify


logger = getLogger(__name__)

# Discord interaction types.
INTERACTION_PING = 1
INTERACTION_APPLICATION_COMMAND = 2

# Discord interaction response types.
RESPONSE_PONG = 1
RESPONSE_CHANNEL_MESSAGE = 4

# Discord message flags.
FLAG_EPHEMERAL = 64


@method_decorator(csrf_exempt, name="dispatch")
class InteractionsView(NeverCacheMixin, View):
    """Handle inbound Discord interaction webhooks.

    Discord sends HTTPS POST requests to this endpoint for slash-command
    interactions and periodic PING health-checks.  Each request carries
    an Ed25519 signature that is verified before any processing.

    CSRF must be exempted because Discord does not (and cannot) provide
    a Django CSRF token.  ``@method_decorator(csrf_exempt)`` is applied
    at the class level so the attribute propagates to the view function
    returned by ``as_view()`` — applying ``@csrf_exempt`` directly to
    ``dispatch()`` does **not** work because Django's CSRF middleware
    inspects the outer view callable, not the dispatch method.
    """

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs) -> JsonResponse:
        # Verify Ed25519 signature from Discord.
        try:
            verify(request)
        except BadSignatureError:
            logger.exception("Invalid Discord signature")
            return JsonResponse(
                data={"error": "Invalid signature."},
                status=401,
            )
        except ValueError:
            logger.exception("Missing Discord signature data")
            return JsonResponse(
                data={"error": "Missing signature."},
                status=400,
            )

        payload = json.loads(request.body)
        interaction_type = payload.get("type")

        # Ping/pong (used by Discord to validate the endpoint).
        if interaction_type == INTERACTION_PING:
            return JsonResponse(
                data={"type": RESPONSE_PONG},
                status=200,
            )

        # Slash commands.
        if interaction_type == INTERACTION_APPLICATION_COMMAND:
            try:
                message, ephemeral = slash(
                    interaction_json=payload,
                    request=request,
                )
            except LookupError:
                logger.exception("Unknown Discord slash command")
                message = "Unknown command."
                ephemeral = True
            except Exception:
                logger.exception("Discord slash command failed")
                message = "Something went wrong."
                ephemeral = True

            response_data = {
                "type": RESPONSE_CHANNEL_MESSAGE,
                "data": {"content": message},
            }
            if ephemeral:
                response_data["data"]["flags"] = FLAG_EPHEMERAL

            return JsonResponse(data=response_data, status=200)

        # Unknown interaction type.
        logger.error("Unknown Discord interaction type: %s", interaction_type)
        return JsonResponse(
            data={"error": "Unknown interaction."},
            status=400,
        )
