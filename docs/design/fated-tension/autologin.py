"""Verification-only middleware: ?as=<account_name> logs that account in,
so headless screenshots can reach the login-gated pages."""
from django.contrib.auth import login

from apps.accounts.models import Account


class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        name = request.GET.get("as")
        if name:
            account = Account.objects.filter(account_name=name).first()
            if account is not None:
                login(request, account, backend="apps.accounts.backends.IsharUserAuthBackend")
        return self.get_response(request)
