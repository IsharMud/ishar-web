"""isharmud.com root URL configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from ishar.apps.core.views import ErrorView


urlpatterns = [
    # isharmud.com URL configuration.
    path("", include("ishar.apps.core.urls"), name="ishar"),

    # Django-Admin.
    path("admin/", admin.site.urls, name="admin"),

    path("i18n/", include('django.conf.urls.i18n')),

    # Redirect to web client.
    path(
        "connect/", RedirectView.as_view(url=settings.CONNECT_URL),
        name="connect"
    ),
]

# Error handlers
handler400 = ErrorView.as_view(
    message="Sorry, but the request was not understood.",
    status_code=400,
    title="Bad Request"
)
handler401 = ErrorView.as_view(
    message="Sorry, but you do not have authorization to access this page.",
    status_code=401,
    title="Not Authorized"
)
handler403 = ErrorView.as_view(
    message="Sorry, but access to this page is forbidden.",
    status_code=403,
    title="Forbidden"
)
handler404 = ErrorView.as_view(
    message="Sorry, but no such page could be found.",
    status_code=404,
    title="Page Not Found"
)
handler405 = ErrorView.as_view(
    message="Sorry, but the requested method is not supported.",
    status_code=405,
    title="Method Not Allowed"
)
handler410 = ErrorView.as_view(
    message="Sorry, but that resource is gone.",
    status_code=410,
    title="Gone"
)
handler420 = ErrorView.as_view(
    message="Sorry, but please enhance your calm.",
    status_code=420,
    title="Enhance Your Calm"
)
handler500 = ErrorView.as_view(
    message= "Sorry, but unfortunately, there was an internal server error.",
    status_code=500,
    title="Sorry!"
)
handler501 = ErrorView.as_view(
    message= "Sorry, but the server cannot handle your request.",
    status_code=501,
    title="Not Implemented"
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path("400/", handler400, name="400"),
    urlpatterns += path("401/", handler401, name="401"),
    urlpatterns += path("403/", handler403, name="403"),
    urlpatterns += path("404/", handler404, name="404"),
    urlpatterns += path("405/", handler405, name="405"),
    urlpatterns += path("410/", handler410, name="410"),
    urlpatterns += path("420/", handler420, name="420"),
    urlpatterns += path("500/", handler500, name="500"),
    urlpatterns += path("501/", handler501, name="501"),
