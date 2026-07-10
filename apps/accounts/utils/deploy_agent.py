"""Client for the host deploy agent (#1754).

The God-gated deploy page (apps/accounts/views/deploy.py) uses this to talk to
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


def ping():
    """Liveness + allowlist discovery."""
    return _call({"action": "ping"})


def start_deploy(actor, env, services, no_pull=False):
    """Ask the agent to start a deploy. Returns the agent's JSON (deploy_id on
    success, or a rejection with an `error` key)."""
    return _call({
        "action": "deploy",
        "actor": actor,
        "env": env,
        "services": services,
        "no_pull": no_pull,
    })


def deploy_status(deploy_id):
    """Poll a running/finished deploy by id."""
    return _call({"action": "status", "deploy_id": deploy_id})
