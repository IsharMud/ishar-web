"""
isharmud.com URL configuration.
"""
from django.contrib import admin
from django.urls import include, path

from .api import api_router
from .views import WelcomeView


urlpatterns = [
    path("", WelcomeView.as_view(), name="index"),
    path("accounts/", include("django.contrib.auth.urls"), name="accounts"),
    path("admin/", admin.site.urls, name="admin"),
    path("api/", include(api_router.urls), name="api")
]
