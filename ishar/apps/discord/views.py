import json
import logging
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.utils.timesince import timeuntil
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from ishar.apps.events.models import GlobalEvent
from ishar.apps.players.models import Player
from ishar.apps.seasons.models import Season


class InteractionsView(View):
    """
    Interactions view.
    """
    DISCORD = settings.DISCORD
    http_method_names = ("get", "post")

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def error(self, message="Invalid request.", status=400) -> JsonResponse:
        logging.error("%s (%s)" % (message, status))
        return JsonResponse(data={"error": message}, status=status)

    def get(self, *args, **kwargs) -> JsonResponse:
        return self.error(message="Method not supported.", status=405)

    def handle_command(self, interaction_data, request):

        command_name = interaction_data.get("name")

        # "deadhead" command - player with most deaths.
        if command_name == "deadhead":
            dead_head = Player.objects.filter(
                true_level__lt=min(settings.IMMORTAL_LEVELS)[0],
            ).order_by("-deaths").first()
            return self.respond(
                "%s :skull_crossbones: %i times!" % (
                    dead_head.name,
                    dead_head.deaths
                )
            )

        # "events" command - any active events and when they expire.
        elif command_name == "events":
            global_events = GlobalEvent.objects.filter(
                start_time__lt=now(),
                end_time__gt=now()
            ).all()

            if global_events.count() > 0:
                reply = "%i events:\n" % (global_events.count())
                events = enumerate(global_events.all(), start=1)
                for (num, event) in events:
                    reply += "%i. %s - ends %s :alarm_clock: %s.\n" % (
                        num,
                        event.event_desc,
                        timeuntil(event.end_time),
                        event.end_time.strftime("%c %Z")
                    )
                return self.respond(reply)

            return self.respond("Sorry - no events right now.")

        # "faq" command to link frequently asked questions.
        elif command_name == "faq":
            return self.respond(
                message="%s://%s%s" % (
                    request.scheme,
                    request.get_host(),
                    reverse("faq")
                )
            )

        # "mudtime" command to show server (UTC) time.
        elif command_name == "mudtime":
            message = now().strftime("%c :clock: %Z")

        # "season" command - shows season number and expiration.
        elif command_name == "season":
            season = Season.objects.filter(is_active=1).first()
            message = (
                "Season %i :hourglass_flowing_sand: "
                "ends %s :alarm_clock: %s." % (
                    season.season_id,
                    timeuntil(season.expiration_date),
                    season.expiration_date.strftime("%c %Z")
                )
            )

        else:
            return self.error(message="Invalid command", status=400)

        return self.respond(message)

    def respond(self, message=None, msg_type=4, status=200) -> JsonResponse:
        if message is not None:
            return JsonResponse(
                data={
                    "type": msg_type,
                    "data": {
                        "content": message
                    }
                },
                status=status
            )
        return self.error()

    def pong(self) -> JsonResponse:
        return JsonResponse({"type": 1})

    def post(self, request, *args, **kwargs) -> JsonResponse:

        verify = self.validate(request)
        if verify is None:
            return self.error("Missing signature.", status=400)
        if verify is False:
            return self.error("Invalid signature.", status=400)
        if verify is not True:
            return self.error(
                "Signature could not be verified.", status=500
            )

        # Get the contents of the interaction and its type, if valid signature.
        interaction_body = json.loads(request.body.decode("utf-8"))
        interaction_type = interaction_body.get("type")

        # Reply to ping with pong, for URL endpoint validation by Discord.
        if interaction_type == 1:
            return self.pong()

        # Reply to slash commands.
        if interaction_type == 2:
            return self.handle_command(
                request=request,
                interaction_data=interaction_body.get("data"),
            )

        return self.error("Invalid command.", status=400)

    def validate(self, request):
        """
        Verify signature via headers of incoming Discord HTTPS requests.
        """
        verify_key = VerifyKey(bytes.fromhex(self.DISCORD["PUBLIC_KEY"]))
        signature = request.headers.get("X-Signature-Ed25519")
        timestamp = request.headers.get("X-Signature-Timestamp")
        body = request.body.decode("utf-8")

        if not signature or not timestamp or not body:
            return None

        try:
            string = f"{timestamp}{body}".encode()
            if verify_key.verify(string, bytes.fromhex(signature)):
                return True

        except (BadSignatureError, ValueError) as bad_sig:
            logging.exception(bad_sig)

        return False
