"""
isharmud.com root URL configuration.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [

    # isharmud.com URL configuration.
    path("", include("ishar.urls"), name="ishar"),

    # Django-Admin.
    path("admin/", admin.site.urls, name="admin"),

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
    )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
