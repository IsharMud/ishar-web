"""
Trial review dashboard — the Eternal+ queue of applications, overdue first.
"""
from django.db.models import Count, Q
from django.utils import timezone
from django.views.generic.list import ListView

from apps.core.views.mixins import EternalRequiredMixin, NeverCacheMixin

from ..models import OPEN_STATUSES, TrialApplication, TrialStatus, TrialTrack


def _overdue_q():
    return Q(status=TrialStatus.SUBMITTED, due_at__lt=timezone.now())


# Which application subsets the "show" filter exposes.
SHOW_FILTERS = {
    "open": Q(status__in=OPEN_STATUSES),
    "submitted": Q(status=TrialStatus.SUBMITTED),
    "needs_revision": Q(status=TrialStatus.NEEDS_REVISION),
    "decided": Q(status__in=(
        TrialStatus.ACCEPTED, TrialStatus.REJECTED, TrialStatus.WITHDRAWN,
    )),
    "all": Q(),
}


class TrialReviewDashboardView(EternalRequiredMixin, NeverCacheMixin, ListView):
    """Staff-facing list of trial applications with filters and counts."""

    context_object_name = "applications"
    http_method_names = ("get",)
    model = TrialApplication
    paginate_by = 25
    template_name = "trial_review_dashboard.html"

    def get_queryset(self):
        params = self.request.GET
        qs = TrialApplication.objects.select_related("account").annotate(
            num_comments=Count("comment"),
        )

        show = params.get("show", "open")
        qs = qs.filter(SHOW_FILTERS.get(show, SHOW_FILTERS["open"]))

        track = params.get("track")
        if track in TrialTrack.values:
            qs = qs.filter(track=track)

        query = (params.get("q") or "").strip()
        if query:
            search = (
                Q(character_name__icontains=query)
                | Q(proposal__icontains=query)
            )
            if query.lstrip("#").isdigit():
                search |= Q(pk=int(query.lstrip("#")))
            qs = qs.filter(search)

        # Default model ordering (due_at, -id) floats overdue reviews to the
        # top of the open queue; decided views read best newest-first.
        if show in ("decided", "all"):
            return qs.order_by("-id")
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # One round trip for all four tiles instead of four COUNT queries.
        counts = TrialApplication.objects.aggregate(
            open=Count("pk", filter=SHOW_FILTERS["open"]),
            overdue=Count("pk", filter=_overdue_q()),
            needs_revision=Count("pk", filter=SHOW_FILTERS["needs_revision"]),
            accepted=Count("pk", filter=Q(status=TrialStatus.ACCEPTED)),
        )
        context.update({
            "tracks": TrialTrack.choices,
            "show_filters": [
                (key, key.replace("_", " ").title()) for key in SHOW_FILTERS
            ],
            "current": {
                "show": self.request.GET.get("show", "open"),
                "track": self.request.GET.get("track", ""),
                "q": self.request.GET.get("q", ""),
            },
            "counts": counts,
        })
        return context
