from django.views.generic.base import TemplateView

from apps.news.models import News


class HomeView(TemplateView):
    """Home page includes latest news post."""
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news"] = News.objects.latest()
        return context
