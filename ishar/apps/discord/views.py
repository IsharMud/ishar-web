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

        body = request.body
        signature = request.headers.get("X-Signature-Ed25519")
        timestamp = request.headers.get("X-Signature-Timestamp")
        if not signature or not timestamp:
            raise SuspiciousOperation("Missing signature.")

        print("body:", body)

        json_body = json.loads(body)
        print("json_body:", json_body)

        in_type = json_body["type"]
        print("in_type:", in_type)

        print("signature:", signature)
        print("timestamp:", timestamp)

        verify = VerifyKey(bytes.fromhex(settings.DISCORD["PUBLIC_KEY"]))
        string = f"{timestamp}{body}".encode()

        try:
            verify = verify.verify(string, bytes.fromhex(signature))
            print("verify:", verify)
            return JsonResponse(data={"body": "ok"}, status_code=200)

        except (BadSignatureError,) as ex:
            raise SuspiciousOperation("Bad signature.") from ex
