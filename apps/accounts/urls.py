from django.urls import path

from .views.deploy import DeployActionView, DeployStatusView, DeployView
from .views.password import PasswordView
from .views.portal import PortalView
from .views.private import SetPrivateView


urlpatterns = [
    path("", PortalView.as_view(), name="portal"),
    path("account/", PortalView.as_view(), name="account"),
    path("password/", PasswordView.as_view(), name="password"),
    path("private/", SetPrivateView.as_view(), name="set_private"),
    path("deploy/", DeployView.as_view(), name="deploy"),
    path("deploy/run/", DeployActionView.as_view(), name="deploy_run"),
    path("deploy/status/", DeployStatusView.as_view(), name="deploy_status"),
]
