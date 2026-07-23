"""Web deploy console (#1754, #1868).

A phone-friendly page (NOT Django admin) where staff pick an environment and
services and trigger scripts/deploy.sh on the host via the deploy agent. Prod
runs on the local host agent; staging is a separate box the agent forwards to
(#1868). The page floor is Eternal, but a *prod* deploy requires Forger — the
per-env gate is enforced here, not just disabled in the UI. The deploy POST
requires password re-entry (re-auth), so a driven/XSS'd session cannot fire a
deploy on its own — see docs/infrastructure/reboot_process.md §4.
"""
import json
from datetime import timedelta

from django.conf import settings
from django.db import DatabaseError
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.generic.base import TemplateView, View

from apps.connect import tracker as connect_tracker
from apps.core.models.webadmin import WebAdminCommand
from apps.core.utils import webadmin
from apps.core.utils.staff import staff_name
from apps.core.views.mixins import EternalRequiredMixin, NeverCacheMixin

from ..utils.deploy_agent import (
    DeployAgentError,
    cancel_deploy,
    deploy_status,
    ping,
    start_deploy,
)

# Scheduled-reboot delay bounds (seconds): 1 minute .. 1 hour. Mirrored by the
# host agent (0..3600) and the game-side clamp/validation.
SCHEDULE_DELAY_MIN = 60
SCHEDULE_DELAY_MAX = 3600

# DEPLOY_ENVIRONMENTS[env]["gate"] -> the Account predicate that gates deploying
# that env. immortal_level is the sole source of truth (game-owned column).
GATE_METHODS = {"eternal": "is_eternal", "forger": "is_forger", "god": "is_god"}


def _resolve_deploy_env(request):
    """Resolve the POSTed console env for a *mutating* deploy and enforce its
    gate (prod → Forger, staging → Eternal). Returns (spec, error_response) with
    exactly one non-None. This is the real authorization boundary; the UI only
    disables the control an account can't use."""
    key = request.POST.get("env", "")
    spec = settings.DEPLOY_ENVIRONMENTS.get(key)
    if spec is None:
        return None, JsonResponse({"message": "Unknown environment."}, status=400)
    if not getattr(request.user, GATE_METHODS[spec["gate"]])():
        return None, JsonResponse(
            {"message": f"Deploying {key} requires {spec['gate'].title()} or higher."},
            status=403,
        )
    return spec, None


def _poll_target(request):
    """Forward target for a status/cancel poll. A forwarded deploy's state lives
    in the remote agent, so the poll must reach the same agent the deploy ran on.
    Read-only, so no gate; an absent/unknown env falls back to the local agent."""
    spec = settings.DEPLOY_ENVIRONMENTS.get(request.POST.get("env", ""))
    return spec["target"] if spec else "local"


class DeployView(EternalRequiredMixin, NeverCacheMixin, TemplateView):
    """Render the deploy control page. Eternal floor (EternalRequiredMixin ->
    404); a prod deploy additionally requires Forger (enforced in the actions)."""

    template_name = "deploy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Show every env, but mark which ones this account may actually deploy
        # (a disabled control + note beats hiding it). The default selection is
        # the first env the account can deploy — prod for a Forger, staging for
        # an Eternal. Services are the union across envs, each tagged with the
        # envs it belongs to so the UI can show only the relevant ones.
        envs = []
        service_order = []
        service_envs = {}
        default_taken = False
        for key, spec in settings.DEPLOY_ENVIRONMENTS.items():
            allowed = getattr(user, GATE_METHODS[spec["gate"]])()
            checked = allowed and not default_taken
            default_taken = default_taken or checked
            envs.append({
                "key": key,
                "icon": spec["icon"],
                "gate": spec["gate"].title(),
                "allowed": allowed,
                "checked": checked,
            })
            for svc in spec["services"]:
                if svc not in service_envs:
                    service_envs[svc] = []
                    service_order.append(svc)
                service_envs[svc].append(key)

        context["deploy_envs"] = envs
        context["deploy_locked"] = [e for e in envs if not e["allowed"]]
        context["deploy_services"] = [
            {"name": s, "envs": " ".join(service_envs[s]), "checked": s == "ishar-app"}
            for s in service_order
        ]
        context["deploy_env_meta"] = json.dumps({
            key: {"target": spec["target"], "services": list(spec["services"]),
                  "schedulable": spec["target"] == "local"}
            for key, spec in settings.DEPLOY_ENVIRONMENTS.items()
        })
        context["deploy_configured"] = bool(settings.DEPLOY_AGENT_SECRET)
        return context


class DeployActionView(EternalRequiredMixin, NeverCacheMixin, View):
    """POST-only endpoint that starts a deploy. CSRF-protected (no exemption).

    Requires re-authentication (password) AND the target env's gate (Forger for
    prod). Env/service validation and injection inertness live in the host agent
    — the local one for prod, the forwarded remote for staging; we surface its
    verdict.
    """

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        # Re-auth: password re-entry on the deploy POST itself.
        password = request.POST.get("password", "")
        if not password or not request.user.check_password(password):
            return JsonResponse(
                {"message": "Re-authentication failed."}, status=403
            )

        spec, err = _resolve_deploy_env(request)
        if err:
            return err

        services = request.POST.getlist("services")
        bad = [s for s in services if s not in spec["services"]]
        if bad:
            return JsonResponse(
                {"message": f"Service(s) not available on this env: {', '.join(bad)}"},
                status=400,
            )
        no_pull = request.POST.get("no_pull") in ("1", "true", "on")

        try:
            result = start_deploy(
                actor=request.user.get_username(),
                env=spec["env"],
                services=services,
                no_pull=no_pull,
                target=spec["target"],
            )
        except DeployAgentError as exc:
            return JsonResponse(
                {"message": f"Deploy agent unavailable: {exc}"}, status=503
            )

        # The agent returns http_status inside its JSON; mirror it so the page
        # sees the real accepted/rejected outcome (busy, cooldown, invalid, ...).
        status = int(result.get("http_status", 200 if result.get("ok") else 400))
        return JsonResponse(result, status=status)


class DeployPingView(EternalRequiredMixin, NeverCacheMixin, View):
    """POST-only liveness probe for the host agent. Powers the console's live
    agent-health pill. Read-only (no re-auth); Eternal gate + CSRF still apply."""

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


class DeployWebClientsView(EternalRequiredMixin, NeverCacheMixin, View):
    """POST-only count of live web-client (/connect) game sessions.

    Deploying ishar-web restarts Daphne, which severs every browser player's
    telnet proxy mid-game — the console polls this to warn before that happens.
    Reads an in-process registry (Daphne is a single process; see
    apps.connect.tracker), so it costs nothing and needs no agent or DB.
    Read-only (no re-auth); Eternal gate + CSRF still apply.
    """

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        return JsonResponse(connect_tracker.snapshot())


class DeployScheduleView(EternalRequiredMixin, NeverCacheMixin, View):
    """POST-only: schedule a deploy after a delay, warning players first.

    Prod-only: the countdown is announced to the live game, which is meaningless
    for staging (a separate box with no prod players), so a non-local target is
    rejected. One action, two effects, in this order:
      1. Ask the host agent to schedule the deploy (it holds the timer and fires
         deploy.sh itself after the delay — surviving this container restarting).
      2. Only if that was accepted, enqueue a `reboot_notice` so the game counts
         the reboot down to the world. Agent-first means we never announce a
         reboot that the agent then refuses (busy/cooldown).

    Requires re-auth (password), exactly like an immediate deploy — scheduling
    commits to an unattended run, so it is gated just as hard.
    """

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        # Re-auth: password re-entry, same as an immediate deploy.
        password = request.POST.get("password", "")
        if not password or not request.user.check_password(password):
            return JsonResponse(
                {"message": "Re-authentication failed."}, status=403
            )

        spec, err = _resolve_deploy_env(request)
        if err:
            return err
        if spec["target"] != "local":
            return JsonResponse(
                {"message": "Scheduling with a player warning is prod-only."},
                status=400,
            )

        delay_raw = request.POST.get("delay_seconds", "")
        if not delay_raw.isdigit():
            return JsonResponse({"message": "Invalid delay."}, status=400)
        delay_seconds = int(delay_raw)
        if not SCHEDULE_DELAY_MIN <= delay_seconds <= SCHEDULE_DELAY_MAX:
            return JsonResponse(
                {"message": "Delay must be between 1 and 60 minutes."}, status=400
            )

        services = request.POST.getlist("services")
        bad = [s for s in services if s not in spec["services"]]
        if bad:
            return JsonResponse(
                {"message": f"Service(s) not available on this env: {', '.join(bad)}"},
                status=400,
            )
        no_pull = request.POST.get("no_pull") in ("1", "true", "on")

        # 1. Schedule the deploy on the host agent (the part that can be refused).
        try:
            result = start_deploy(
                actor=request.user.get_username(),
                env=spec["env"],
                services=services,
                no_pull=no_pull,
                delay_seconds=delay_seconds,
                target=spec["target"],
            )
        except DeployAgentError as exc:
            return JsonResponse(
                {"message": f"Deploy agent unavailable: {exc}"}, status=503
            )

        status = int(result.get("http_status", 200 if result.get("ok") else 400))
        if status != 200 or not result.get("ok"):
            # Busy / cooldown / invalid — nothing announced to players.
            return JsonResponse(result, status=status)

        # 2. Deploy is scheduled — now warn the world via the game.
        task = webadmin.enqueue(
            command=WebAdminCommand.REBOOT_NOTICE,
            payload={"delay_seconds": delay_seconds},
            actor_account=request.user.account_id,
            actor_name=staff_name(request.user),
        )
        return JsonResponse({**result, "notice_task_id": task.id}, status=200)


class DeployCancelScheduledView(EternalRequiredMixin, NeverCacheMixin, View):
    """POST-only: cancel a still-scheduled deploy and tell players it's off.

    Cancels the host agent's pending deploy (a no-op once it has started
    running), then — if the cancel landed on a prod (local) deploy — enqueues a
    `reboot_cancel` so the game announces the stand-down. No re-auth: cancelling
    is the safe direction. Eternal gate + CSRF still apply.
    """

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        deploy_id = request.POST.get("deploy_id", "")
        if not deploy_id:
            return JsonResponse({"message": "Missing deploy_id."}, status=400)

        target = _poll_target(request)
        try:
            result = cancel_deploy(deploy_id, target=target)
        except DeployAgentError as exc:
            return JsonResponse(
                {"message": f"Deploy agent unavailable: {exc}"}, status=503
            )

        # Only prod deploys are scheduled (and thus announced), so only they get
        # a stand-down announcement.
        if result.get("ok") and target == "local":
            webadmin.enqueue(
                command=WebAdminCommand.REBOOT_CANCEL,
                payload={},
                actor_account=request.user.account_id,
                actor_name=staff_name(request.user),
            )

        status = int(result.get("http_status", 200 if result.get("ok") else 409))
        return JsonResponse(result, status=status)


class DeployGameStatusView(EternalRequiredMixin, NeverCacheMixin, View):
    """POST-only read of the game's presence heartbeat (Contract 2, #1771).

    Powers the console's live "Game" pill and the pre-deploy warning when
    ishar-app is selected with players in-game (closes the game-side half of
    #77). The game publishes game_status (a singleton heartbeat) and
    game_presence (one row per in-game character); we report whether the game
    is up (heartbeat within the staleness window), the live player count, and
    the heartbeat age. Degrades gracefully before the game ships the heartbeat
    (tables absent / no row). Read-only (no re-auth); Eternal gate + CSRF apply.
    """

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        # Imported here so a web deploy that predates the game migration can't
        # break module import; the query itself is guarded below.
        from apps.players.models.presence import (
            GamePresence,
            GameStatus,
            PRESENCE_STALE_SECONDS,
        )

        cutoff = now() - timedelta(seconds=PRESENCE_STALE_SECONDS)
        try:
            status = GameStatus.objects.filter(pk=1).first()
        except DatabaseError:
            # Tables not created yet (web deployed before the game migration).
            return JsonResponse({"integrated": False, "up": False, "player_count": 0})

        if status is None:
            # Migration ran but the game hasn't booted with presence yet.
            return JsonResponse({"integrated": False, "up": False, "player_count": 0})

        beat_age = max(0, int((now() - status.heartbeat_at).total_seconds()))
        up = beat_age <= PRESENCE_STALE_SECONDS

        player_count = 0
        if up:
            try:
                player_count = GamePresence.objects.filter(
                    last_seen__gte=cutoff
                ).count()
            except DatabaseError:
                player_count = 0

        return JsonResponse(
            {
                "integrated": True,
                "up": up,
                "player_count": player_count,
                "beat_age": beat_age,
            }
        )


class DeployStatusView(EternalRequiredMixin, NeverCacheMixin, View):
    """POST-only status poll for a running/finished deploy. No re-auth (read
    only); Eternal gate + CSRF still apply. Carries the deploy's env so a
    forwarded (staging) deploy is polled on the agent that holds its state."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        deploy_id = request.POST.get("deploy_id", "")
        if not deploy_id:
            return JsonResponse({"message": "Missing deploy_id."}, status=400)
        try:
            result = deploy_status(deploy_id, target=_poll_target(request))
        except DeployAgentError as exc:
            return JsonResponse(
                {"message": f"Deploy agent unavailable: {exc}"}, status=503
            )
        status = int(result.get("http_status", 200 if result.get("ok") else 404))
        return JsonResponse(result, status=status)
