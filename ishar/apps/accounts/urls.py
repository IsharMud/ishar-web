from django.urls import path

from .views import AccountView, PasswordView, PortalView


urlpatterns = [
    path("", PortalView.as_view(), name="portal"),
    path("account/", AccountView.as_view(), name="account"),
    path("password/", PasswordView.as_view(), name="password"),
]
