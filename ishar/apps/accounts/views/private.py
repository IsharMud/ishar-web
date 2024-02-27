from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from ..models.account import Account


class SetPrivateView(LoginRequiredMixin, View):

    http_method_names = ("post",)
    message = "Unknown Error"
    status = 400

    def post(self, request, *args, **kwargs):

        if request.user and request.user.is_authenticated:

            account = Account.objects.get(account_id=request.user.account_id)

            if not request.user.is_private:
                account.is_private = True
            elif request.user.is_private:
                account.is_private = False
            account.save()

            self.message = {"is_private": account.is_private}
            self.status = 200

        return JsonResponse(data={"message": self.message}, status=self.status)
