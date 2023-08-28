"""
URL configuration for isharmud.com project.
"""
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('isharweb.urls'), name='isharweb'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('admin/', admin.site.urls, name='admin'),
]
