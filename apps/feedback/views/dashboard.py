"""
Feedback triage dashboard — the filterable, sortable table of reports.
"""
from django.db.models import Count, Q
from django.views.generic.list import ListView

from apps.core.views.mixins import EternalRequiredMixin, NeverCacheMixin

from ..models import Feedback, FeedbackState, FeedbackType


# Which report subsets the "show" filter exposes, and how each scopes the query.
SHOW_FILTERS = {
    "active": Q(state__in=(FeedbackState.OPEN, FeedbackState.IN_PROGRESS)),
    "open": Q(state=FeedbackState.OPEN),
    "in_progress": Q(state=FeedbackState.IN_PROGRESS),
    "closed": Q(state=FeedbackState.CLOSED),
    "all": Q(),
}

# Optional quick flags layered on top of the "show" filter.
FLAG_FILTERS = {
    "unacked": Q(state=FeedbackState.OPEN, acknowledged_by__isnull=True),
    "bountied": Q(bountied=True),
    "private": Q(is_private=True),
    "promoted": Q(github_issue_url__isnull=False),
}

SORTS = {
    "newest": "-id",
    "oldest": "id",
    "level": "-player_level",
}


class FeedbackDashboardView(EternalRequiredMixin, NeverCacheMixin, ListView):
    """Staff-facing list of feedback reports with filters and counts."""

    context_object_name = "reports"
    http_method_names = ("get",)
    model = Feedback
    paginate_by = 25
    template_name = "feedback_dashboard.html"

    def get_queryset(self):
        params = self.request.GET
        qs = Feedback.objects.all().annotate(num_comments=Count("comment"))

        show = params.get("show", "active")
        qs = qs.filter(SHOW_FILTERS.get(show, SHOW_FILTERS["active"]))

        ftype = params.get("type")
        if ftype in FeedbackType.values:
            qs = qs.filter(feedback_type=ftype)

        flag = params.get("flag")
        if flag in FLAG_FILTERS:
            qs = qs.filter(FLAG_FILTERS[flag])

        source = params.get("source")
        if source in ("game", "discord"):
            qs = qs.filter(source=source)

        query = (params.get("q") or "").strip()
        if query:
            search = Q(body__icontains=query) | Q(player_name__icontains=query)
            if query.lstrip("#").isdigit():
                search |= Q(pk=int(query.lstrip("#")))
            qs = qs.filter(search)

        return qs.order_by(SORTS.get(params.get("sort"), "-id"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # One round trip for all four tiles instead of four COUNT queries.
        counts = Feedback.objects.aggregate(
            active=Count("pk", filter=SHOW_FILTERS["active"]),
            unacked=Count("pk", filter=FLAG_FILTERS["unacked"]),
            in_progress=Count("pk", filter=SHOW_FILTERS["in_progress"]),
            bountied=Count("pk", filter=FLAG_FILTERS["bountied"]),
        )
        context.update({
            "feedback_types": FeedbackType.choices,
            "show_filters": [
                (key, key.replace("_", " ").title()) for key in SHOW_FILTERS
            ],
            "flag_filters": tuple(FLAG_FILTERS.keys()),
            "current": {
                "show": self.request.GET.get("show", "active"),
                "type": self.request.GET.get("type", ""),
                "flag": self.request.GET.get("flag", ""),
                "source": self.request.GET.get("source", ""),
                "sort": self.request.GET.get("sort", "newest"),
                "q": self.request.GET.get("q", ""),
            },
            "counts": counts,
        })
        return context
