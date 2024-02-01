import json
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
        timestamp = request.headers["X-Signature-Timestamp"]
        body = request.body.decode("utf-8")

        if not signature or not timestamp or not body:
            raise SuspiciousOperation("Missing signature.")

        try:
            verify_key.verify(
                f'{timestamp}{body}'.encode(), bytes.fromhex(signature)
            )
            return JsonResponse({"type": 1})

        except BadSignatureError:
            return JsonResponse(
                data={"error": "Invalid request method"},
                status=405
            )
