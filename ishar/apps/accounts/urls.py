from django.urls import path

from .views import IsharLoginView, IsharLogoutView, PortalView


urlpatterns = [
    path("", PortalView.as_view(), name="portal"),
    path("login/", IsharLoginView.as_view(), name="login"),
    path("logout/", IsharLogoutView.as_view(), name="logout"),
]
