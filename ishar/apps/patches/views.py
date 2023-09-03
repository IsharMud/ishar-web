from django.views.generic.base import TemplateView

from .util import get_patch_pdfs, get_patch_pdf


class PatchView(TemplateView):
    template_name = "patches.html.djt"
    extra_context = {"patches": get_patch_pdfs()}


class LatestPatchView(TemplateView):
    template_name = "latest.html.djt"
    pdfs = get_patch_pdfs()
    if pdfs and pdfs[0]:
        extra_context = {"pdf": pdfs[0]}


class TextPatchView(TemplateView):
    template_name = "pdf.html.djt"
    pdf = get_patch_pdf()
    if pdf:
        extra_context = {"pdf": pdf}
