from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic.base import View

from ..models.account import Account


class SetPrivateView(LoginRequiredMixin, View):
    """
    Set private view.
    Used by "portal" template via JavaScript AJAX/XMLHttpRequest ("XHR").
    """

    # Only handle POST requests.
    http_method_names = ("post",)

    # Default message and response code indicate failure.
    message = "Unknown Error"
    status = 400

    def post(self, request, *args, **kwargs):
        """Handle POST HTTP requests."""

        # Ensure user is authenticated.
        if request.user and request.user.is_authenticated:

            # Gather account object.
            account = Account.objects.get(account_id=request.user.account_id)

            # Toggle "is_private" on account, depending on user's current value.
            if not request.user.is_private:
                account.is_private = True
            elif request.user.is_private:
                account.is_private = False

            # Save only "is_private" field on the account object.
            account.save(update_fields=("is_private",))

            # Set reply message, and successful HTTP response status code.
            self.message = {"is_private": account.is_private}
            self.status = 200

        # Return the message within JSON, using appropriate HTTP status code.
        return JsonResponse(data={"message": self.message}, status=self.status)
