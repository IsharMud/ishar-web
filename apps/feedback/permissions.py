"""
Access gates for the feedback triage dashboard.

Mirrors the in-game command levels: the `reports` command requires
`LEVEL_ETERNAL`, and `reports claude` additionally requires `LEVEL_GOD`
(ishar-mud `src/kernel/wizard.c`). On the website those map to
`Account.is_eternal()` and `Account.is_god()`.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from apps.core.views.mixins import NeverCacheMixin


class StaffFeedbackMixin(LoginRequiredMixin, NeverCacheMixin):
    """Eternal (or above) may triage feedback — mirrors `LEVEL_ETERNAL`."""

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated or not user.is_eternal():
            raise PermissionDenied(
                "Feedback triage is restricted to Eternal staff and above."
            )
        return super().dispatch(request, *args, **kwargs)


def requires_god(action) -> bool:
    """Which triage actions are Gods-only. Only 'assign_claude', matching the
    `reports claude` gate in the game."""
    return action == "assign_claude"
