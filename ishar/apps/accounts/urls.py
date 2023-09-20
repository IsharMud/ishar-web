from django.urls import path

from .views import IsharLoginView, IsharLogoutView, PortalView, AccountView, \
    PasswordView


urlpatterns = [
    path("", PortalView.as_view(), name="portal"),
    path("account/", AccountView.as_view(), name="account"),
    path("password/", PasswordView.as_view(), name="password")
]
