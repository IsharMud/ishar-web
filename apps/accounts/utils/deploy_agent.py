"""Client for the host deploy agent (#1754).

The Forger-gated deploy page (apps/accounts/views/deploy.py) uses this to talk to
scripts/deploy-agent.py on the host over a bind-mounted unix socket. The agent —
NOT this container — is the real security boundary: it enforces the env/service
allowlist and argv-execs deploy.sh. This client only frames JSON requests and
attaches the shared secret from settings; it never logs the secret and never
returns it to the browser.
"""
import json
import socket

from django.conf import settings


class DeployAgentError(Exception):
    """The deploy agent is unconfigured, unreachable, or spoke gibberish."""


def _call(payload, timeout=15):
    sock_path = getattr(settings, "DEPLOY_AGENT_SOCKET", "")
    secret = getattr(settings, "DEPLOY_AGENT_SECRET", "")
    if not sock_path or not secret:
        raise DeployAgentError("deploy agent is not configured")

    body = dict(payload)
    body["secret"] = secret

    chunks = []
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect(sock_path)
            sock.sendall(json.dumps(body).encode("utf-8"))
            sock.shutdown(socket.SHUT_WR)
            while True:
                data = sock.recv(65536)
                if not data:
                    break
                chunks.append(data)
    except (OSError, socket.timeout) as exc:
        raise DeployAgentError(f"cannot reach deploy agent: {exc}") from exc

    try:
        return json.loads(b"".join(chunks).decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise DeployAgentError("invalid response from deploy agent") from exc


def _with_target(payload, target):
    """Tag a request for a remote agent so the local (prod) agent forwards it
    (#1868). "local"/None means handle it here — no target field, wire-identical
    to the pre-forwarding protocol. A forwarded action's state (e.g. a deploy_id)
    lives in the remote agent, so status/cancel for it must carry the same
    target."""
    if target and target != "local":
        payload["target"] = target
    return payload


def ping(target=None):
    """Liveness + allowlist discovery."""
    return _call(_with_target({"action": "ping"}, target))


def start_deploy(actor, env, services, no_pull=False, delay_seconds=0, target=None):
    """Ask the agent to start a deploy. Returns the agent's JSON (deploy_id on
    success, or a rejection with an `error` key).

    With delay_seconds > 0 the agent *schedules* the deploy: it reserves the
    single-flight slot immediately (status "scheduled") and fires deploy.sh
    itself after the delay — surviving this container restarting. Cancel a
    scheduled deploy with cancel_deploy()."""
    return _call(_with_target({
        "action": "deploy",
        "actor": actor,
        "env": env,
        "services": services,
        "no_pull": no_pull,
        "delay_seconds": int(delay_seconds),
    }, target))


def cancel_deploy(deploy_id, target=None):
    """Cancel a still-scheduled deploy before it fires. No-op (409) once it has
    started running. Returns the agent's JSON."""
    return _call(_with_target({"action": "cancel", "deploy_id": deploy_id}, target))


def deploy_status(deploy_id, target=None):
    """Poll a running/finished/scheduled deploy by id."""
    return _call(_with_target({"action": "status", "deploy_id": deploy_id}, target))


# ── Read-only log access (ishar-web#104) ─────────────────────────────────────
# Same agent, socket, and secret as the deploy actions above — the log actions
# are read-only additions. The agent is still the boundary: it allowlists env /
# source / color and argv-execs docker with no shell.


def log_status(env, target=None):
    """Live-color + which colors/web containers are up, plus the source/color
    allowlists. Powers the viewer's LIVE badge and control state."""
    return _call(_with_target({"action": "log-status", "env": env}, target))


def fetch_log(actor, env, source, color="live", lines=500, timeout=25, target=None):
    """Return a byte-capped tail of one log source. `source` is runlog|stderr|web;
    `color` is live|blue|green (ignored for web). The agent re-validates all of
    it. A slightly longer timeout than deploy calls: reading an idle color's
    runlog spins up a throwaway container host-side."""
    return _call(
        _with_target(
            {
                "action": "log-tail",
                "actor": actor,
                "env": env,
                "source": source,
                "color": color,
                "lines": int(lines),
            },
            target,
        ),
        timeout=timeout,
    )
