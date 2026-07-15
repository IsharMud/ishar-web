from django.urls import path

from .views.dashboard import DashboardView
from .views.deploy import (
    DeployActionView,
    DeployCancelScheduledView,
    DeployGameStatusView,
    DeployPingView,
    DeployScheduleView,
    DeployStatusView,
    DeployView,
    DeployWebClientsView,
)
from .views.logs import LogFetchView, LogStatusView, LogViewerView
from .views.password import PasswordView
from .views.portal import PortalView
from .views.private import SetPrivateView


urlpatterns = [
    path("", PortalView.as_view(), name="portal"),
    path("account/", PortalView.as_view(), name="account"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("password/", PasswordView.as_view(), name="password"),
    path("private/", SetPrivateView.as_view(), name="set_private"),
    path("deploy/", DeployView.as_view(), name="deploy"),
    path("deploy/run/", DeployActionView.as_view(), name="deploy_run"),
    path("deploy/schedule/", DeployScheduleView.as_view(), name="deploy_schedule"),
    path(
        "deploy/cancel-scheduled/",
        DeployCancelScheduledView.as_view(),
        name="deploy_cancel_scheduled",
    ),
    path("deploy/status/", DeployStatusView.as_view(), name="deploy_status"),
    path("deploy/ping/", DeployPingView.as_view(), name="deploy_ping"),
    path(
        "deploy/web-clients/",
        DeployWebClientsView.as_view(),
        name="deploy_web_clients",
    ),
    path(
        "deploy/game-status/",
        DeployGameStatusView.as_view(),
        name="deploy_game_status",
    ),
    path("logs/", LogViewerView.as_view(), name="logs"),
    path("logs/status/", LogStatusView.as_view(), name="logs_status"),
    path("logs/fetch/", LogFetchView.as_view(), name="logs_fetch"),
]
