"""God-gated web deploy button (#1754).

A phone-friendly page (NOT Django admin) where a God picks an environment and
services and triggers scripts/deploy.sh on the host via the deploy agent. The
deploy POST requires password re-entry (re-auth), so a driven/XSS'd session
cannot fire a deploy on its own — see docs/infrastructure/reboot_process.md §4.
"""
from django.conf import settings
from django.http import JsonResponse
from django.views.generic.base import TemplateView, View

from apps.core.views.mixins import GodRequiredMixin, NeverCacheMixin

from ..utils.deploy_agent import DeployAgentError, deploy_status, ping, start_deploy


class DeployView(GodRequiredMixin, NeverCacheMixin, TemplateView):
    """Render the deploy control page. God-only (GodRequiredMixin -> 404)."""

    template_name = "deploy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deploy_envs"] = settings.DEPLOY_AGENT_ENVS
        context["deploy_services"] = settings.DEPLOY_AGENT_SERVICES
        context["deploy_configured"] = bool(settings.DEPLOY_AGENT_SECRET)
        return context


class DeployActionView(GodRequiredMixin, NeverCacheMixin, View):
    """POST-only endpoint that starts a deploy. CSRF-protected (no exemption).

    Requires re-authentication: the God must re-enter their account password on
    this request. The heavy validation (env/service allowlist, injection
    inertness) lives in the host agent; we surface its verdict.
    """

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        # Re-auth: password re-entry on the deploy POST itself.
        password = request.POST.get("password", "")
        if not password or not request.user.check_password(password):
            return JsonResponse(
                {"message": "Re-authentication failed."}, status=403
            )

        env = request.POST.get("env", "")
        services = request.POST.getlist("services")
        no_pull = request.POST.get("no_pull") in ("1", "true", "on")

        try:
            result = start_deploy(
                actor=request.user.get_username(),
                env=env,
                services=services,
                no_pull=no_pull,
            )
        except DeployAgentError as exc:
            return JsonResponse(
                {"message": f"Deploy agent unavailable: {exc}"}, status=503
            )

        # The agent returns http_status inside its JSON; mirror it so the page
        # sees the real accepted/rejected outcome (busy, cooldown, invalid, ...).
        status = int(result.get("http_status", 200 if result.get("ok") else 400))
        return JsonResponse(result, status=status)


class DeployPingView(GodRequiredMixin, NeverCacheMixin, View):
    """POST-only liveness probe for the host agent. Powers the console's live
    agent-health pill. Read-only (no re-auth); God gate + CSRF still apply."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        try:
            result = ping()
        except DeployAgentError as exc:
            return JsonResponse(
                {"ok": False, "message": f"Deploy agent unavailable: {exc}"},
                status=503,
            )
        # Normalize: guarantee an `ok` flag for the pill regardless of the
        # agent's own shape.
        if "ok" not in result:
            result = {"ok": True, **result}
        return JsonResponse(result)


class DeployStatusView(GodRequiredMixin, NeverCacheMixin, View):
    """POST-only status poll for a running/finished deploy. No re-auth (read
    only); God gate + CSRF still apply."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        deploy_id = request.POST.get("deploy_id", "")
        if not deploy_id:
            return JsonResponse({"message": "Missing deploy_id."}, status=400)
        try:
            result = deploy_status(deploy_id)
        except DeployAgentError as exc:
            return JsonResponse(
                {"message": f"Deploy agent unavailable: {exc}"}, status=503
            )
        status = int(result.get("http_status", 200 if result.get("ok") else 404))
        return JsonResponse(result, status=status)
