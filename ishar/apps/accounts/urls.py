from django.urls import path

from ishar.apps.accounts.views import PasswordView, PortalView


urlpatterns = [
    path("", PortalView.as_view(), name="portal"),
    path("account/", PortalView.as_view(), name="account"),
    path("password/", PasswordView.as_view(), name="password"),
]
