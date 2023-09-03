from django.urls import include, path

from .api import api_router
from .views import PortalView, SupportView, WelcomeView
from .views import ConnectRedirectView
from .views.faq import FAQView


urlpatterns = [
    path("", WelcomeView.as_view(), name="index"),
    # path("account/", include("ishar.apps.account.urls"), name="account"),
    path("api/", include(api_router.urls), name="api"),
    path("connect/", ConnectRedirectView.as_view(), name="connect"),
    # path("events/", EventsView.as_view(), name="events"),
    path("faq/", FAQView.as_view(), name="faq"),
    path("faqs/", FAQView.as_view(), name="faqs"),
    path("questions/", FAQView.as_view(), name="questions"),
    path("help/", include("ishar.apps.help.urls"), name="help"),
    path("patches/", include("ishar.apps.patches.urls"), name="patches",),
    path("portal", PortalView.as_view(), name="portal"),
    path("season/", include("ishar.apps.season.urls"), name="season"),
    path("support/", SupportView.as_view(), name="support"),
    # path("season/", include("ishar.apps.season.urls"), name="season"),
]
