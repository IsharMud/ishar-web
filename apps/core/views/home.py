from django.views.generic.base import TemplateView

from apps.news.models import News


class HomeView(TemplateView):
    """Home page."""
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Include latest news post on main page.
        context = super().get_context_data(**kwargs)
        context["news"] = News.objects.filter(is_visible__exact=True).order_by(
            "-created"
        ).first()
        return context
