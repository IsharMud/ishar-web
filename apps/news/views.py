from django.views.generic.list import ListView

from .models import News


class NewsView(ListView):
    """News list view lists all past news posts."""

    context_object_name = "news_post"
    model = News
    paginate_by = 1
    queryset = model.objects.filter(is_visible__exact=True).all()[1:]
    template_name = "news.html"
