"""JSON endpoint for the HUD action bar (isharmud/ishar-web#167).

The action bar — favorite skills + pinned consumables in numbered slots —
is per-character HUD state, so it keys on the connected character rather
than the account (a player's mage and warrior want different bars). The
client knows only the character's GMCP name; this view resolves it to a
``players`` row **owned by the requesting account**, which both authorizes
the request and yields the stable ``player_id`` the bar keys on.

``GET  ?character=<name>`` → the saved slots (``found: false`` when the
character has no server bar yet — the client's cue to seed the row from the
browser's pre-migration localStorage). ``POST {character, slots}`` upserts,
with the slot list re-sanitized here: the stored blob is never trusted from
the client (mirrors ``hud.js`` ``normalizeSlot``).
"""
import json

from django.http import JsonResponse
from django.views.generic.base import View

from apps.core.views.mixins import NeverCacheMixin
from apps.players.models import Player

from ..models import HudBar
from .map import MapJSONMixin


# Mirrors hud.js SLOT_MAX (two pages of ten). A longer list is truncated.
SLOT_MAX = 20

# Per-field caps for a pinned-item slot object (mirrors hud.js normalizeSlot).
_KEY_MAX = 64
_CMD_MAX = 64
_NAME_MAX = 64
_OTYPE_MAX = 32
_ICON_MAX = 64


def _str_field(value, cap):
    return value[:cap] if isinstance(value, str) else ""


def _sanitize_slot(x):
    """One slot -> a stored skill key (str), item object (dict), or None.

    The client blob is untrusted: skill keys are capped, item objects are
    rebuilt field-by-field, and anything else collapses to an empty slot.
    """
    if isinstance(x, str):
        x = x.strip()
        return x[:_KEY_MAX] if x else None
    if isinstance(x, dict) and x.get("item") is True:
        cmd = x.get("cmd")
        if not isinstance(cmd, str) or not cmd.strip():
            return None
        vnum = x.get("vnum")
        if isinstance(vnum, bool) or not isinstance(vnum, int):
            vnum = None
        return {
            "item": True,
            "cmd": cmd.strip()[:_CMD_MAX],
            "vnum": vnum,
            "otype": _str_field(x.get("otype"), _OTYPE_MAX),
            "name": _str_field(x.get("name"), _NAME_MAX),
            "icon": _str_field(x.get("icon"), _ICON_MAX),
        }
    return None


def _sanitize_slots(raw):
    if not isinstance(raw, list):
        return []
    return [_sanitize_slot(x) for x in raw[:SLOT_MAX]]


class HudBarView(MapJSONMixin, NeverCacheMixin, View):
    """Per-character action-bar load (GET) and save (POST)."""

    http_method_names = ("get", "post")

    def _player_id(self, request, name):
        """``players.id`` for a character name owned by the request's
        account, or None. The account scope is the authorization boundary —
        an account may only read/write bars for its own characters."""
        if not isinstance(name, str) or not name.strip():
            return None
        return (
            Player.objects.filter(
                account_id=request.user.account_id,
                name__iexact=name.strip(),
                is_deleted=False,
            ).values_list("id", flat=True).first()
        )

    def get(self, request, *args, **kwargs):
        player_id = self._player_id(request, request.GET.get("character"))
        if player_id is None:
            return JsonResponse({"error": "unknown character"}, status=404)
        slots = HudBar.objects.filter(player_id=player_id).values_list(
            "slots", flat=True,
        ).first()
        if slots is None:
            return JsonResponse({"found": False, "slots": [], "max": SLOT_MAX})
        return JsonResponse({"found": True, "slots": slots, "max": SLOT_MAX})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            name = data["character"]
            slots = data["slots"]
        except (json.JSONDecodeError, KeyError, TypeError, UnicodeDecodeError):
            return JsonResponse({"error": "bad request"}, status=400)

        player_id = self._player_id(request, name)
        if player_id is None:
            return JsonResponse({"error": "unknown character"}, status=404)

        HudBar.objects.update_or_create(
            player_id=player_id,
            defaults={
                "account_id": request.user.account_id,
                "slots": _sanitize_slots(slots),
            },
        )
        return JsonResponse({"ok": True, "max": SLOT_MAX})
