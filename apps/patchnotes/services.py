"""
Patch-notes service layer — the web mirror of `patch_notes.rs`.

State writes are direct (the game queries `patch_notes` live, so a Django write
is instantly visible in-game — no command queue needed). The one thing the web
container cannot do is post to Discord, so `publish()` uses a transactional
outbox: it flips the note published AND enqueues one `patch_notes_sync_queue`
row in the same transaction, and the game replays the announcement.

Per-account read state (`account_patch_notes_read`, composite PK) is handled
with raw SQL here — the same `INSERT IGNORE` / anti-join the game uses — rather
than fighting Django's single-column-PK assumption with a model.
"""
from django.db import connection, transaction
from django.utils import timezone

from .models import PatchNote, PatchNoteSyncTask

READ_TABLE = "account_patch_notes_read"


# --------------------------------------------------------------------------- #
# Per-account read state (raw SQL — mirrors patch_notes.rs)
# --------------------------------------------------------------------------- #

def mark_read(account_id: int, note_id: int) -> None:
    """Mark one note read for an account (idempotent). Mirrors mark_as_read."""
    if not account_id or not note_id:
        return
    with connection.cursor() as cur:
        cur.execute(
            f"INSERT IGNORE INTO {READ_TABLE} (account_id, patch_note_id) "
            "VALUES (%s, %s)",
            [account_id, note_id],
        )


def mark_all_read(account_id: int) -> int:
    """Mark every published note read for an account. Returns rows inserted."""
    if not account_id:
        return 0
    with connection.cursor() as cur:
        cur.execute(
            f"INSERT IGNORE INTO {READ_TABLE} (account_id, patch_note_id) "
            "SELECT %s, id FROM patch_notes WHERE is_published = 1",
            [account_id],
        )
        return cur.rowcount or 0


def unread_count(account_id: int) -> int:
    """Count published notes this account has not read. Mirrors count_unread."""
    if not account_id:
        return 0
    with connection.cursor() as cur:
        cur.execute(
            "SELECT COUNT(*) FROM patch_notes pn WHERE pn.is_published = 1 "
            f"AND pn.id NOT IN (SELECT patch_note_id FROM {READ_TABLE} "
            "WHERE account_id = %s)",
            [account_id],
        )
        row = cur.fetchone()
    return int(row[0]) if row else 0


def read_ids(account_id: int, note_ids) -> set:
    """Return the subset of `note_ids` this account has already read."""
    note_ids = [int(n) for n in note_ids]
    if not account_id or not note_ids:
        return set()
    placeholders = ", ".join(["%s"] * len(note_ids))
    with connection.cursor() as cur:
        cur.execute(
            f"SELECT patch_note_id FROM {READ_TABLE} "
            f"WHERE account_id = %s AND patch_note_id IN ({placeholders})",
            [account_id, *note_ids],
        )
        return {r[0] for r in cur.fetchall()}


# --------------------------------------------------------------------------- #
# Authoring (direct state writes)
# --------------------------------------------------------------------------- #

def create_draft(title: str, body: str, author: str, season_id=None) -> PatchNote:
    """Create an unpublished draft. `created_at` set explicitly (managed=False:
    Django would otherwise send NULL past the DB's CURRENT_TIMESTAMP default)."""
    return PatchNote.objects.create(
        title=title[:80],
        body=body,
        author=(author or "System")[:30],
        is_published=False,
        season_id=season_id,
        created_at=timezone.now(),
    )


def update_note(note: PatchNote, title: str, body: str, season_id) -> None:
    """Edit a note's content (narrow write)."""
    note.title = title[:80]
    note.body = body
    note.season_id = season_id
    note.save(update_fields=("title", "body", "season_id"))


def publish(note: PatchNote, actor: str) -> bool:
    """
    Publish a draft: flip it published AND enqueue the Discord announcement in
    one transaction (transactional outbox). Returns False if already published
    (idempotent — re-clicking Publish is a no-op, never a duplicate announce).
    """
    if note.is_published:
        return False
    with transaction.atomic():
        note.is_published = True
        note.published_at = timezone.now()
        note.save(update_fields=("is_published", "published_at"))
        PatchNoteSyncTask.objects.create(
            patch_note=note,
            action=PatchNoteSyncTask.Action.PUBLISH,
            actor=(actor or "System")[:64],
            status=PatchNoteSyncTask.Status.PENDING,
            created_at=timezone.now(),
        )
    return True


def unpublish(note: PatchNote) -> None:
    """Revert a note to draft (hides it from players). No Discord unsend."""
    note.is_published = False
    note.save(update_fields=("is_published",))


def delete_note(note: PatchNote) -> None:
    """Delete a note. The DB FKs cascade read-state and any queue rows."""
    note.delete()
