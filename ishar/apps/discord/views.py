import json
import logging
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


class InteractionsView(View):
    """
    Interactions view.
    """
    http_method_names = ("post",)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        verify_key = VerifyKey(bytes.fromhex(settings.DISCORD["PUBLIC_KEY"]))

        signature = request.headers.get("X-Signature-Ed25519")
        timestamp = request.headers.get("X-Signature-Timestamp")
        body = request.body.decode("utf-8")

        if not signature or not timestamp or not body:
            logging.info("Missing signature.")
            return JsonResponse(data={"error": "Invalid request."}, status=400)

        try:
            string = f"{timestamp}{body}".encode()
            verify_key.verify(string, bytes.fromhex(signature))
            logging.info("KEY OK.")
            logging.debug(body)
            return JsonResponse({"type": 1})

        except BadSignatureError as bad_sig:
            logging.exception(bad_sig)
            return JsonResponse(data={"error": "Invalid request."}, status=400)
