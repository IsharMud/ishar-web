"""
Live style guide — staff-only page rendering every design token and Admin
Console component from docs/design/, so a consistent page is copy-paste away
and visual regressions are eyeballed in one place.
"""
from django.views.generic.base import TemplateView

from .mixins import EternalRequiredMixin, NeverCacheMixin


class StyleGuideView(EternalRequiredMixin, NeverCacheMixin, TemplateView):
    """The design system, rendered live (Eternal+)."""

    template_name = "styleguide.html"
