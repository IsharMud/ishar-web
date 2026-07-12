"""
Enqueue/cancel helpers for the `web_admin_queue` outbox.

The consoles call `enqueue()` from their POST action views; the game drains
the row on its next game-minute pulse and writes `status`/`result` back for
the console's poll endpoint. `cancel()` is a guarded update that only lands
while the row is still `pending` — it races safely against the game's own
claim, which is guarded the same way.
"""
from django.db import transaction
from django.utils import timezone

from apps.core.models.webadmin import WebAdminStatus, WebAdminTask


def enqueue(command: str, payload: dict, actor_account: int,
            actor_name: str) -> WebAdminTask:
    """Insert one pending command row and return it."""
    with transaction.atomic():
        return WebAdminTask.objects.create(
            command=command,
            payload=payload or None,
            actor_account=actor_account,
            actor_name=actor_name[:64],
            status=WebAdminStatus.PENDING,
            # The game table is NOT NULL DEFAULT CURRENT_TIMESTAMP; Django
            # would otherwise send NULL.
            created_at=timezone.now(),
        )


def cancel(task_id: int, actor_name: str) -> bool:
    """Cancel a still-pending command. Returns whether anything was
    cancelled (False = already claimed/processed by the game)."""
    updated = WebAdminTask.objects.filter(
        id=task_id,
        status=WebAdminStatus.PENDING,
    ).update(
        status=WebAdminStatus.CANCELLED,
        result=f"cancelled by {actor_name}"[:255],
        processed_at=timezone.now(),
    )
    return bool(updated)
