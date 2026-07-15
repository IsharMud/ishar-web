"""
Patch-notes web views.

Public viewer (anyone can read published notes; read-tracking + unread markers
only when logged in) and a staff editor/publisher that does every admin action
the in-game `news` command supports: draft, edit, publish (-> Discord via the
game), unpublish, delete. Publishing writes state directly and enqueues the
Discord announcement — see `services.publish`.

The editor mirrors the Deploy Console pattern: POST-only CBVs returning
`JsonResponse`, CSRF via the `X-CSRFToken` header, `EternalRequiredMixin`
(matching the in-game LEVEL_ETERNAL floor -> 404 for everyone else).
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from apps.core.utils.staff import staff_name
from apps.core.views.mixins import EternalRequiredMixin, NeverCacheMixin

from .markdown import body_to_html
from .models import PatchNote
from .services import (
    create_draft,
    delete_note,
    mark_all_read,
    mark_read,
    publish,
    read_ids,
    unpublish,
    update_note,
)

# Season id sanity bound (the game's season_id is a small positive int).
SEASON_MAX = 99_999


def _parse_season(raw):
    """Blank -> None; a positive int within range -> int; else raises ValueError."""
    raw = (raw or "").strip()
    if not raw:
        return None
    if not raw.isdigit():
        raise ValueError("Season must be a number.")
    value = int(raw)
    if not 1 <= value <= SEASON_MAX:
        raise ValueError("Season is out of range.")
    return value


# --------------------------------------------------------------------------- #
# Public viewer
# --------------------------------------------------------------------------- #

class PatchNotesListView(ListView):
    """Published patch notes, newest first. Public; read markers when logged in."""

    model = PatchNote
    context_object_name = "notes"
    paginate_by = 10
    template_name = "patchnotes/list.html"
    queryset = PatchNote.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notes = list(context.get("notes") or [])
        user = self.request.user
        if user.is_authenticated:
            read = read_ids(user.account_id, [n.pk for n in notes])
            for note in notes:
                note.is_read = note.pk in read
            context["show_read_state"] = True
        else:
            for note in notes:
                note.is_read = True
            context["show_read_state"] = False
        return context


class PatchNoteDetailView(DetailView):
    """A single published patch note. Reading it marks it read for the account."""

    model = PatchNote
    context_object_name = "note"
    template_name = "patchnotes/detail.html"
    queryset = PatchNote.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            mark_read(request.user.account_id, self.object.pk)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["body_html"] = body_to_html(self.object.body)
        return context


class MarkAllReadView(LoginRequiredMixin, NeverCacheMixin, View):
    """POST-only: mark every published note read for the current account."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        marked = mark_all_read(request.user.account_id)
        return JsonResponse({"ok": True, "marked": marked})


# --------------------------------------------------------------------------- #
# Staff editor / publisher (Eternal+; 404 for everyone else)
# --------------------------------------------------------------------------- #

class PatchNoteConsoleView(EternalRequiredMixin, NeverCacheMixin, TemplateView):
    """The Patch Note editor page: every note (drafts + published) + authoring."""

    template_name = "patchnotes/console.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notes = list(PatchNote.objects.all())
        context["notes"] = notes
        # Editable payloads for the "Edit" buttons, serialized safely via
        # json_script (avoids stuffing multiline bodies into data- attributes).
        context["note_data"] = [
            {
                "id": note.pk,
                "title": note.title,
                "season": note.season_id or "",
                "body": note.body,
            }
            for note in notes
        ]
        return context


class _NoteActionView(EternalRequiredMixin, NeverCacheMixin, View):
    """Shared base for the POST action endpoints."""

    http_method_names = ("post",)

    def get_note(self, request):
        pk = request.POST.get("id", "")
        if not pk.isdigit():
            return None
        return PatchNote.objects.filter(pk=int(pk)).first()


class PatchNoteCreateView(_NoteActionView):
    """Create a draft."""

    def post(self, request, *args, **kwargs):
        title = (request.POST.get("title") or "").strip()
        body = request.POST.get("body") or ""
        if not title:
            return JsonResponse({"message": "Title is required."}, status=400)
        if not body.strip():
            return JsonResponse({"message": "Body is required."}, status=400)
        try:
            season_id = _parse_season(request.POST.get("season_id"))
        except ValueError as exc:
            return JsonResponse({"message": str(exc)}, status=400)

        note = create_draft(title, body, staff_name(request.user), season_id)
        return JsonResponse(
            {"ok": True, "id": note.pk, "message": f"Draft #{note.pk} created."}
        )


class PatchNoteUpdateView(_NoteActionView):
    """Edit a note's title / body / season."""

    def post(self, request, *args, **kwargs):
        note = self.get_note(request)
        if note is None:
            return JsonResponse({"message": "Patch note not found."}, status=404)
        title = (request.POST.get("title") or "").strip()
        body = request.POST.get("body") or ""
        if not title:
            return JsonResponse({"message": "Title is required."}, status=400)
        if not body.strip():
            return JsonResponse({"message": "Body is required."}, status=400)
        try:
            season_id = _parse_season(request.POST.get("season_id"))
        except ValueError as exc:
            return JsonResponse({"message": str(exc)}, status=400)

        update_note(note, title, body, season_id)
        return JsonResponse({"ok": True, "id": note.pk, "message": f"Note #{note.pk} saved."})


class PatchNotePublishView(_NoteActionView):
    """Publish a draft: flip published + enqueue the Discord announcement."""

    def post(self, request, *args, **kwargs):
        note = self.get_note(request)
        if note is None:
            return JsonResponse({"message": "Patch note not found."}, status=404)
        if not publish(note, staff_name(request.user)):
            return JsonResponse(
                {"ok": True, "id": note.pk, "already": True,
                 "message": f"Note #{note.pk} is already published."}
            )
        return JsonResponse(
            {"ok": True, "id": note.pk, "published": True,
             "message": f"Note #{note.pk} published. Discord announcement queued."}
        )


class PatchNoteUnpublishView(_NoteActionView):
    """Revert a note to draft (hide from players). No Discord unsend."""

    def post(self, request, *args, **kwargs):
        note = self.get_note(request)
        if note is None:
            return JsonResponse({"message": "Patch note not found."}, status=404)
        unpublish(note)
        return JsonResponse(
            {"ok": True, "id": note.pk, "message": f"Note #{note.pk} reverted to draft."}
        )


class PatchNoteDeleteView(_NoteActionView):
    """Delete a note (cascades read-state and any queue rows)."""

    def post(self, request, *args, **kwargs):
        note = self.get_note(request)
        if note is None:
            return JsonResponse({"message": "Patch note not found."}, status=404)
        note_id = note.pk
        delete_note(note)
        return JsonResponse({"ok": True, "id": note_id, "message": f"Note #{note_id} deleted."})
