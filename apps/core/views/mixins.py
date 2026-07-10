from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic.base import View


@method_decorator(never_cache, name="dispatch")
class NeverCacheMixin(View):
    pass


class GodRequiredMixin(View):
    """Restrict a view to God-level accounts (immortal_level >= GOD).

    Everyone else — authenticated non-Gods AND anonymous users — gets a plain
    404, so the deploy surface's existence is not disclosed (consistent for the
    page and its endpoints, per #1754). This is the project's first staff-gating
    view mixin; game-DB immortal_level is the sole source of truth (see
    apps/accounts/models/account.py: is_god()).
    """

    def dispatch(self, request, *args, **kwargs):
        user = getattr(request, "user", None)
        if not (user and user.is_authenticated and user.is_god()):
            raise Http404
        return super().dispatch(request, *args, **kwargs)
