from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from apps.core.views.mixins import NeverCacheMixin
from apps.fated.context import account_tension_context


class PortalView(LoginRequiredMixin, NeverCacheMixin, TemplateView):
    template_name = "portal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tension"] = account_tension_context(self.request.user)
        return context
