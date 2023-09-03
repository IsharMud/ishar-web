from django.views.generic.base import TemplateView

from .util import get_patch_pdfs, get_patch_pdf


class PatchView(TemplateView):
    template_name = "patches.html.djt"
    extra_context = {"patches": get_patch_pdfs()}


class LatestPatchView(TemplateView):
    template_name = "latest.html.djt"
    extra_context = {"pdf": get_patch_pdfs()[0]}


class TextPatchView(TemplateView):
    template_name = "pdf.html.djt"
    extra_context = {"pdf": get_patch_pdf()}
