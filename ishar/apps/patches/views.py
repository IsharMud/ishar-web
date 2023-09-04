from django.views.generic.base import TemplateView

from .models import Patch


class PatchView(TemplateView):
    template_name = "patches.html.djt"
    extra_context = {"patches": Patch.objects.all()}
