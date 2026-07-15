"""Staff log viewer (ishar-web#104).

A phone-friendly, Eternal-gated page that reads the game/web logs through the
host agent's read-only `log-status` / `log-tail` actions (the same agent and
socket the deploy console uses). The web container can't see the per-color log
volumes, run docker, or read the proxy's live-color state itself — the agent is
the boundary and the bridge.

Shape mirrors the deploy console: a TemplateView for the page, and small
POST-only, `JsonResponse`-returning, CSRF-protected, gated action views. These
are read-only (no re-auth), like the deploy console's ping/status probes.
"""
from django.conf import settings
from django.http import JsonResponse
from django.views.generic.base import TemplateView, View

from apps.core.views.mixins import EternalRequiredMixin, NeverCacheMixin

from ..utils.deploy_agent import DeployAgentError, fetch_log, log_status
from ..utils.log_parse import LEVELS, parse_log

# Line-count presets offered in the UI. The agent clamps to its own max.
LINE_CHOICES = (200, 500, 1000, 2000, 5000)
DEFAULT_LINES = 500
COLORS = ("live", "blue", "green")

# The host agent is a long-lived process that a deploy does NOT restart (it can't
# deploy itself — see scripts/deploy-agent.py and the systemd unit). So a checkout
# that has the log actions but a still-running old agent process answers `bad-action`
# to log-status/log-tail. Turn that opaque rejection into an actionable message
# instead of a bare "agent error", so the failure is self-diagnosing.
_OUTDATED_AGENT_HINT = (
    "The host log agent doesn't recognize the log actions — it's running an "
    "outdated deploy-agent.py. On the host, update the checkout and restart it: "
    "sudo systemctl restart ishar-deploy-agent"
)


def _agent_version_hint(payload):
    """Return an actionable message when the agent rejected the action as unknown
    (an outdated agent), else None."""
    if isinstance(payload, dict) and payload.get("error") == "bad-action":
        return _OUTDATED_AGENT_HINT
    return None


class LogViewerView(EternalRequiredMixin, NeverCacheMixin, TemplateView):
    """Render the log viewer. Eternal-gated (staff); unauthorized -> 404."""

    template_name = "logs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["log_sources"] = settings.LOG_VIEWER_SOURCES
        context["log_line_choices"] = LINE_CHOICES
        context["log_default_lines"] = DEFAULT_LINES
        context["log_levels"] = LEVELS
        context["log_configured"] = bool(settings.DEPLOY_AGENT_SECRET)
        return context


class LogStatusView(EternalRequiredMixin, NeverCacheMixin, View):
    """POST-only: report the live color and which containers are up. Powers the
    LIVE badge and enables/disables the color toggle. Read-only; CSRF + gate."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        try:
            result = log_status(settings.LOG_VIEWER_ENV)
        except DeployAgentError as exc:
            return JsonResponse(
                {"ok": False, "message": f"Log agent unavailable: {exc}"},
                status=503,
            )
        status = int(result.get("http_status", 200 if result.get("ok") else 400))
        hint = _agent_version_hint(result)
        if hint:
            result = {**result, "message": hint}
        return JsonResponse(result, status=status)


class LogFetchView(EternalRequiredMixin, NeverCacheMixin, View):
    """POST-only: fetch and parse a log tail. Allowlists source/color/lines, then
    lets the agent re-validate authoritatively. Read-only; CSRF + gate."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        source = request.POST.get("source", "")
        color = request.POST.get("color", "live")
        if source not in settings.LOG_VIEWER_SOURCES:
            return JsonResponse({"message": "Unknown log source."}, status=400)
        if color not in COLORS:
            return JsonResponse({"message": "Unknown color."}, status=400)

        raw = request.POST.get("lines", str(DEFAULT_LINES))
        try:
            lines = max(1, min(int(raw), max(LINE_CHOICES)))
        except (TypeError, ValueError):
            lines = DEFAULT_LINES

        try:
            data = fetch_log(
                actor=request.user.get_username(),
                env=settings.LOG_VIEWER_ENV,
                source=source,
                color=color,
                lines=lines,
            )
        except DeployAgentError as exc:
            return JsonResponse(
                {"message": f"Log agent unavailable: {exc}"}, status=503
            )

        if not data.get("ok"):
            status = int(data.get("http_status", 502))
            hint = _agent_version_hint(data)
            return JsonResponse(
                {**data, "message": hint or data.get("detail") or "Log unavailable."},
                status=status,
            )

        parsed = parse_log(data.get("text", ""), source)
        return JsonResponse(
            {
                "ok": True,
                "source": data.get("source"),
                "color": data.get("color"),
                "live_color": data.get("live_color"),
                "container": data.get("container"),
                "running": data.get("running"),
                "truncated": data.get("truncated", False),
                "note": data.get("note"),
                "lines_requested": lines,
                **parsed,
            }
        )
