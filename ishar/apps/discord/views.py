import json
import os

from django.conf import settings
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

        print(vars(request))

        code = 400
        ret = ""
        body = request.body
        sig = request.headers.get("X-Signature-Ed25519")
        ts = request.headers.get("X-Signature-Timestamp")
        vk = VerifyKey(bytes.fromhex(settings.DISCORD["PUBLIC_KEY"]))

        print("body:", body)
        print("sig:", sig)
        print("ts:", ts)
        print("vk:", vk)

        try:
            if vk.verify(f"{ts}{body}".encode(), bytes.fromhex(sig)):
                code = 200
                ret = "OK"
        except (BadSignatureError,) as ex:
            ret = ex

        return JsonResponse(
            data={"body": ret},
            status=code,
            status_code=code,
        )
