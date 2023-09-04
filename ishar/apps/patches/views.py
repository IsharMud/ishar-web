from django.views.generic.base import TemplateView

from .models import Patch


class PatchView(TemplateView):
    template_name = "patches.html.djt"
    patches = Patch.objects.all()
    extra_context = {"patches": patches}
