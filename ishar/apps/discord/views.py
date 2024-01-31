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

    @staticmethod
    def post(request, *args, **kwargs):
        print(vars(request))
        if kwargs:
            for kwarg in kwargs:
                print(vars(kwarg))

        return JsonResponse(
            {
                "ping": "pong"
            }
        )
