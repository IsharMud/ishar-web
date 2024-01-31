from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View


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

        signature = request.headers.get("X-Signature-Ed25519")
        timestamp = request.headers.get("X-Signature-Timestamp")

        print("Signature:", signature)
        print("Timestamp:", timestamp)
        print("kwargs:", kwargs)

        if kwargs:
            for kwarg in kwargs:
                print("kwarg:", vars(kwarg))

        return JsonResponse(
            {
                "ping": "pong"
            }
        )
