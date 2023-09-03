from django.views.generic.base import TemplateView

from ..models import Season


class SeasonView(TemplateView):
    template_name = "season.html.djt"
    extra_context = {"season": Season.objects.first()}
