"""
isharmud.com root URL configuration.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.views.generic import RedirectView

from ishar.views import (
    Error400BadRequestView, Error401NotAuthorizedView, Error403ForbiddenView,
    Error404PageNotFoundView, Error405MethodNotAllowedView, ErrorView
)


urlpatterns = [
    # isharmud.com URL configuration.
    path("", include("ishar.urls"), name="ishar"),

    # Django-Admin.
    path("admin/", admin.site.urls, name="admin"),

    #
    # Flat pages.
    #

    # MUD clients.
    path("clients/", views.flatpage, {"url": "/clients/"}, name="clients"),

    # Support (Ishar MUD).
    path("faq/", views.flatpage, {"url": "/faq/"}, name="faq"),

    # History.
    path("history/", views.flatpage, {"url": "/history/"}, name="history"),

    # Getting started guide.
    path("start/", views.flatpage, {"url": "/start/"}, name="start"),

    # Support (Ishar MUD).
    path("support/", views.flatpage, {"url": "/support/"}, name="support"),

    #
    # Redirects.
    #

    # Connect via web client.
    path(
        "connect/", RedirectView.as_view(url=settings.CONNECT_URL),
        name="connect"
    ),

    # Discord invitation.
    path(
        "discord/", RedirectView.as_view(url=settings.DISCORD['URL']),
        name="discord"
    ),
]

# Error handlers
handler400 = Error400BadRequestView.as_view()
handler401 = Error401NotAuthorizedView.as_view()
handler403 = Error403ForbiddenView.as_view()
handler404 = Error404PageNotFoundView.as_view()
handler405 = Error405MethodNotAllowedView.as_view()
handler500 = ErrorView.as_view()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path("400/", handler400, name="400"),
    urlpatterns += path("401/", handler401, name="401"),
    urlpatterns += path("403/", handler403, name="403"),
    urlpatterns += path("404/", handler404, name="404"),
    urlpatterns += path("405/", handler405, name="405"),
    urlpatterns += path("500/", handler500, name="500"),
