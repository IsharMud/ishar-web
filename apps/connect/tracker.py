"""In-process registry of live web-client (telnet proxy) sessions.

Daphne serves HTTP and WebSocket from a single process (see Dockerfile CMD),
so a module-level registry is visible to both the Channels consumer and the
ordinary Django views — no channel layer or database needed. The Deploy
Console reads this to warn a God that deploying ishar-web will sever every
browser player's game connection mid-session.

Consumers register after the socket is fully accepted (browser attached AND
the game-side telnet connect succeeded), so the count is "players actually
in the game via the web client", not half-open handshakes.
"""
import time
from threading import Lock


_lock = Lock()
_sessions: dict[int, float] = {}  # id(consumer) -> time.monotonic() at accept


def register(consumer) -> None:
    """Record a fully-established web-client session."""
    with _lock:
        _sessions[id(consumer)] = time.monotonic()


def unregister(consumer) -> None:
    """Drop a session. Idempotent — safe on never-registered consumers."""
    with _lock:
        _sessions.pop(id(consumer), None)


def snapshot() -> dict:
    """Return {"count": int, "ages": [seconds, ...]} (ages descending)."""
    now = time.monotonic()
    with _lock:
        ages = sorted((now - t for t in _sessions.values()), reverse=True)
    return {"count": len(ages), "ages": [int(age) for age in ages]}
