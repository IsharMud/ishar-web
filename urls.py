from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path("", include("ishar.urls"), name="ishar"),
    path("admin/", admin.site.urls, name="admin"),
    path(
        "connect/",
        RedirectView.as_view(url=settings.CONNECT_URL),
        name="connect"
    ),
    path(
        "discord/",
        RedirectView.as_view(url=settings.DISCORD['URL']),
        name="discord"
    ),
]
