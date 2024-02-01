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

        signature = request.headers["X-Signature-Ed25519"]
        logging.info(signature)

        timestamp = request.headers["X-Signature-Timestamp"]
        logging.info(timestamp)

        body = request.body.decode("utf-8")
        logging.info(body)

        if not signature or not timestamp or not body:
            msg = "Missing signature"
            logging.info(msg)
            raise SuspiciousOperation(msg)

        try:
            verify_key.verify(
                f"{timestamp}{body}".encode(),
                bytes.fromhex(signature)
            )
            logging.info("KEY OK")
            return JsonResponse({"type": 1})

        except BadSignatureError as bad_sig:
            logging.exception(bad_sig)
            return JsonResponse(data={"error": "Invalid request."}, status=400)
