from django.views.generic.list import ListView

from .models import FAQ


class FAQView(ListView):
    """Frequently Asked Questions view."""

    context_object_name = "faqs"
    model = FAQ
    template_name = "faq.html"

    def get_queryset(self):
        return super().get_queryset().filter(is_visible__exact=1)
