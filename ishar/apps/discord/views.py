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
        discord_public_key = settings.DISCORD["PUBLIC_KEY"]
        sig = request.headers.get("X-Signature-Ed25519")
        ts = request.headers.get("X-Signature-Timestamp")
        if not sig or not ts:
            raise SuspiciousOperation("Bad Signature.")

        print('discord_public_key:', discord_public_key)
        print("body:", body)
        print("sig:", sig)
        print("ts:", ts)

        vk = VerifyKey(bytes.fromhex(discord_public_key))
        print("vk:", vk)

        try:
            verify = vk.verify(f"{ts}{body}".encode(), bytes.fromhex(sig))
            print("verify:", verify)
            return JsonResponse(data={"body": "ok"}, status_code=200)

        except (BadSignatureError,) as ex:
            raise SuspiciousOperation("Bad Signature.") from ex
