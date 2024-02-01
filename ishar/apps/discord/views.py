import json
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from pprint import pformat


class InteractionsView(View):
    """
    Interactions view.
    """
    http_method_names = ("post",)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def error(message="Invalid request.", status=400) -> JsonResponse:
        logging.error("%s (%s)" % (message, status))
        return JsonResponse(data={"error": message}, status=status)

    def post(self, request, *args, **kwargs) -> JsonResponse:
        verify_key = VerifyKey(bytes.fromhex(settings.DISCORD["PUBLIC_KEY"]))
        signature = request.headers.get("X-Signature-Ed25519")
        timestamp = request.headers.get("X-Signature-Timestamp")
        body = request.body.decode("utf-8")

        if not signature or not timestamp or not body:
            return self.error("Missing signature.")

        try:
            string = f"{timestamp}{body}".encode()
            verify_key.verify(string, bytes.fromhex(signature))

        except BadSignatureError as bad_sig:
            logging.exception(bad_sig)
            return self.error("Invalid signature.")

        interaction_body = json.loads(body)
        interaction_type = interaction_body.get("type")

        if interaction_type == 1:
            logging.info("PING: OK!")
            return JsonResponse({"type": 1})

        if interaction_type == 2:
            interaction_data = interaction_body.get("data")
            if interaction_data.get("name") == "season":
                logging.info("Season command.")
                return JsonResponse({
                    "type": 4,
                    "content": "Congrats on sending your command!"
                })
