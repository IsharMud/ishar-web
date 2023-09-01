"""
isharmud.com URL configuration.
"""
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('ishar.urls'), name='ishar'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('admin/', admin.site.urls, name='admin'),
]
