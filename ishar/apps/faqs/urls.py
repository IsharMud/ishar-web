from django.urls import path

from ishar.apps.faqs.views import FAQView


urlpatterns = [
    path("", FAQView.as_view(), name="faq"),
]
