from datetime import datetime
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Schema

from ishar.api import api
from ishar.apps.patches.models import Patch
from ishar.apps.players.api.schemas import PlayerAccountSchema


class PatchSchema(Schema):
    """Patch schema."""
    patch_id: int
    is_visible: bool
    patch_date: datetime
    patch_file: str
    patch_name: str
    account: PlayerAccountSchema


@api.get(
    path="/patch/",
    response=PatchSchema,
    summary="Latest visible patch.",
    tags=["patches"]
)
def latest(request):
    """Latest visible patch."""
    return Patch.objects.filter(
        is_visible__exact=1,
    ).order_by(
        "-patch_date"
    ).first()


@api.get(
    path="/patches/",
    response=List[PatchSchema],
    summary="Any and all patches.",
    tags=["patches"]
)
def patches(request):
    """Any and all patches - including not visible."""
    return Patch.objects.all()


@api.get(
    path="/patches/hidden/",
    response=List[PatchSchema],
    summary="Patches marked as NOT visible.",
    tags=["patches"]
)
def hidden(request):
    """Patches marked as NOT visible."""
    return Patch.objects.exclude(is_visible__exact=1).all()


@api.get(
    path="/patches/visible/",
    response=List[PatchSchema],
    summary="Patches marked as visible.",
    tags=["patches"]
)
def visible(request):
    """Patches marked as visible."""
    return Patch.objects.filter(is_visible__exact=1).all()


@api.get(
    path="/patch/{patch_id}/",
    response=PatchSchema,
    summary="Single patch, by ID.",
    tags=["patches"]
)
def patch(request, patch_id: int):
    """Single patch, by ID."""
    return get_object_or_404(Patch, patch_id=patch_id)
