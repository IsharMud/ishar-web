from django.views.generic.list import ListView
from rest_framework import viewsets, permissions

from ishar.apps.faqs.models import FAQ
from ishar.apps.faqs.serializers import FAQSerializer


class FAQViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows frequently asked questions to be viewed or edited.
    """
    model = FAQ
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = FAQSerializer


class FAQView(ListView):
    """
    Frequently Asked Questions view.
    """
    context_object_name = "faqs"
    model = FAQ
    template_name = "faq.html"

    def get_queryset(self):
        return super().get_queryset().filter(is_visible__exact=1)
