from django.urls import path

from .views.password import PasswordView
from .views.portal import PortalView
from .views.private import SetPrivateView


urlpatterns = [
    path("", PortalView.as_view(), name="portal"),
    path("account/", PortalView.as_view(), name="account"),
    path("password/", PasswordView.as_view(), name="password"),
    path("private/", SetPrivateView.as_view(), name="set_private"),
]
