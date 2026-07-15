from django.urls import path

from .views import (
    MarkAllReadView,
    PatchNoteConsoleView,
    PatchNoteCreateView,
    PatchNoteDeleteView,
    PatchNoteDetailView,
    PatchNotePublishView,
    PatchNoteUnpublishView,
    PatchNoteUpdateView,
    PatchNotesListView,
)


urlpatterns = [
    # Public viewer
    path("", PatchNotesListView.as_view(), name="patch_notes"),
    path("read/", MarkAllReadView.as_view(), name="patch_notes_mark_all_read"),
    path("<int:pk>/", PatchNoteDetailView.as_view(), name="patch_note"),
    # Staff editor / publisher
    path("console/", PatchNoteConsoleView.as_view(), name="patch_notes_console"),
    path("console/create/", PatchNoteCreateView.as_view(), name="patch_note_create"),
    path("console/update/", PatchNoteUpdateView.as_view(), name="patch_note_update"),
    path("console/publish/", PatchNotePublishView.as_view(), name="patch_note_publish"),
    path("console/unpublish/", PatchNoteUnpublishView.as_view(), name="patch_note_unpublish"),
    path("console/delete/", PatchNoteDeleteView.as_view(), name="patch_note_delete"),
]
