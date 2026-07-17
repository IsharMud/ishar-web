"""JSON endpoints for the HUD map (isharmud/ishar-web#125).

Four views back the client-side mapper (``hud-map.js``):

* ``ZoneGraphView`` — the authoritative exit graph of one zone, straight
  from the game's ``rooms`` / ``room_exits`` tables. Hidden exits are
  excluded, exit keys are normalized **byte-identically** to the game's
  ``gmcp_exit_key()`` (telnet.c) so graph edges line up with live
  ``Room.Info`` keys, and the whole response is ETagged — zone content
  changes only on content deploys, so browsers cache it for free.
* ``MapStateView`` — the per-account fog-of-war + notes for one zone.
* ``MapDiscoverView`` / ``MapNoteView`` — POST-only mutations, following
  the ``SetPrivateView`` conventions (JSON body, ``X-CSRFToken`` header,
  strict input validation).

Fog of war is honest-player UX, not security: the full zone graph is in
the graph payload for anyone who opens devtools. Accepted trade-off —
see the ADR in ``docs/design/decisions.md``.
"""
import hashlib
import json
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View

from apps.core.views.mixins import NeverCacheMixin
from apps.rooms.models import Room, RoomExit, RoomExitFlag, RoomFlag, Zone

from ..models import RoomDiscovery, RoomNote


# Terrain tinyint -> display name, in the game's enum order
# (src/include/constants.h terrain_t / src/kernel/constants.c terrainnames).
TERRAIN_NAMES = (
    "Indoor", "City", "Field", "Forest", "Hill", "Mountain",
    "Shallow Water", "Deep Water", "Underwater", "Desert", "Beach",
    "Forest Path", "Mountain Path", "Swamp",
)

# The ten compass/vertical names collapse to short keys, matched
# case-insensitively; every other exit name passes through VERBATIM
# (not lowercased) — byte-identical to gmcp_exit_key() in telnet.c.
COMPASS_KEYS = {
    "north": "n", "south": "s", "east": "e", "west": "w",
    "up": "u", "down": "d",
    "northeast": "ne", "northwest": "nw",
    "southeast": "se", "southwest": "sw",
}

NOTE_MAX_LENGTH = 2000
DISCOVER_MAX_BATCH = 200

# Ishar "@x" color codes; "@@" is a literal "@" (mirrors hud.js stripColor).
_COLOR_RE = re.compile("@.")


def strip_color(s):
    """Strip Ishar ``@x`` color codes; ``@@`` is a literal ``@``."""
    if not s:
        return ""
    return _COLOR_RE.sub(
        lambda m: "@" if m.group(0) == "@@" else "", str(s)
    )


def exit_key(name):
    """Normalize an exit name exactly like the game's ``gmcp_exit_key()``."""
    if not name:
        return None
    return COMPASS_KEYS.get(name.strip().lower(), name)


class MapJSONMixin(LoginRequiredMixin):
    """Login-gated JSON endpoint: an expired session gets a 403, never a
    login-page redirect a ``fetch()`` would silently follow."""

    raise_exception = True


class ZoneGraphView(MapJSONMixin, View):
    """GET the full exit graph of the zone containing a room vnum."""

    http_method_names = ("get",)

    def get(self, request, *args, **kwargs):
        vnum = kwargs["vnum"]
        room = Room.objects.filter(vnum=vnum, is_deleted=False).first()
        if room is None:
            return JsonResponse({"error": "unknown room"}, status=404)

        zone = Zone.objects.filter(id=room.zone_id).first()
        zone_rooms = list(
            Room.objects.filter(
                zone_id=room.zone_id, is_deleted=False,
            ).values("vnum", "name", "terrain")
        )
        zone_vnums = {r["vnum"] for r in zone_rooms}

        room_flags = {
            f["room"]: f
            for f in RoomFlag.objects.filter(room__in=zone_vnums).values(
                "room", "flag_death", "flag_peaceful",
            )
        }
        exit_rows = list(
            RoomExit.objects.filter(room_vnum__in=zone_vnums).values(
                "id", "room_vnum", "exit_name", "destination_vnum",
            )
        )
        exit_flags = {
            f["exit"]: f
            for f in RoomExitFlag.objects.filter(
                exit__in=[e["id"] for e in exit_rows],
            ).values("exit", "flag_door", "flag_closed", "flag_locked",
                     "flag_hidden", "flag_climb")
        }

        # Surviving directed edges: named, visible, and pointing at a room
        # that exists. Deleted destinations are dropped for in-zone edges;
        # cross-zone destinations are validated against `rooms` below.
        edges = []
        for e in exit_rows:
            dest = e["destination_vnum"]
            key = exit_key(e["exit_name"])
            flags = exit_flags.get(e["id"], {})
            if not dest or not key or flags.get("flag_hidden"):
                continue
            edges.append({
                "f": e["room_vnum"], "d": key, "t": dest,
                "door": 1 if flags.get("flag_door") else 0,
                "locked": 1 if flags.get("flag_locked") else 0,
                "climb": 1 if flags.get("flag_climb") else 0,
            })

        # One-way: no surviving reverse edge (any exit name) exists.
        pairs = {(e["f"], e["t"]) for e in edges}

        out_vnums = {e["t"] for e in edges if e["t"] not in zone_vnums}
        out_rooms = {
            r["vnum"]: r["zone_id"]
            for r in Room.objects.filter(
                vnum__in=out_vnums, is_deleted=False,
            ).values("vnum", "zone_id")
        }
        out_zone_names = {
            z["id"]: z["name"]
            for z in Zone.objects.filter(
                id__in=set(out_rooms.values()),
            ).values("id", "name")
        }

        exits, out = [], []
        for e in edges:
            one = 0 if (e["t"], e["f"]) in pairs else 1
            if e["t"] in zone_vnums:
                item = {k: v for k, v in e.items() if v}
                if one:
                    item["one"] = 1
                exits.append(item)
            elif e["t"] in out_rooms:
                dest_zone = out_rooms[e["t"]]
                out.append({
                    "f": e["f"], "d": e["d"], "t": e["t"],
                    "zone": dest_zone,
                    "zname": out_zone_names.get(dest_zone, ""),
                })

        payload = {
            "zone": {
                "id": room.zone_id,
                "name": zone.name if zone else "",
            },
            "rooms": [
                {
                    "v": r["vnum"],
                    "n": strip_color(r["name"]),
                    "t": TERRAIN_NAMES[r["terrain"]]
                    if r["terrain"] is not None
                    and 0 <= r["terrain"] < len(TERRAIN_NAMES)
                    else TERRAIN_NAMES[0],
                    **(
                        {"f": flags}
                        if (flags := [
                            name for name, key in (
                                ("death", "flag_death"),
                                ("peaceful", "flag_peaceful"),
                            ) if room_flags.get(r["vnum"], {}).get(key)
                        ])
                        else {}
                    ),
                }
                for r in zone_rooms
            ],
            "exits": exits,
            "out": out,
        }

        body = json.dumps(payload, separators=(",", ":")).encode()
        etag = f'"{hashlib.md5(body).hexdigest()}"'
        if request.headers.get("If-None-Match") == etag:
            response = HttpResponse(status=304)
        else:
            response = HttpResponse(body, content_type="application/json")
        response["ETag"] = etag
        response["Cache-Control"] = "private, max-age=3600"
        return response


class MapStateView(MapJSONMixin, NeverCacheMixin, View):
    """GET the account's fog-of-war + notes for one zone."""

    http_method_names = ("get",)

    def get(self, request, *args, **kwargs):
        zone_id = kwargs["zone_id"]
        account_id = request.user.account_id
        discovered = list(
            RoomDiscovery.objects.filter(
                account_id=account_id, zone_id=zone_id,
            ).values_list("room_vnum", flat=True)
        )
        notes = {
            str(n["room_vnum"]): n["text"]
            for n in RoomNote.objects.filter(
                account_id=account_id, zone_id=zone_id,
            ).values("room_vnum", "text")
        }
        return JsonResponse({"discovered": discovered, "notes": notes})


class MapDiscoverView(MapJSONMixin, NeverCacheMixin, View):
    """POST a batch of freshly-visited room vnums."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            rooms = data["rooms"]
        except (json.JSONDecodeError, KeyError, TypeError, UnicodeDecodeError):
            return JsonResponse({"error": "bad request"}, status=400)
        if (
            not isinstance(rooms, list)
            or len(rooms) > DISCOVER_MAX_BATCH
            or not all(
                isinstance(v, int) and not isinstance(v, bool)
                and 0 < v < 10**9
                for v in rooms
            )
        ):
            return JsonResponse({"error": "bad request"}, status=400)

        # Resolve zones server-side; unknown vnums are silently dropped.
        zones = dict(
            Room.objects.filter(
                vnum__in=rooms, is_deleted=False,
            ).values_list("vnum", "zone_id")
        )
        account_id = request.user.account_id
        added = RoomDiscovery.objects.bulk_create(
            [
                RoomDiscovery(
                    account_id=account_id, room_vnum=v, zone_id=zones[v],
                )
                for v in set(rooms) if v in zones
            ],
            ignore_conflicts=True,
        )
        return JsonResponse({"ok": True, "added": len(added)})


class MapNoteView(MapJSONMixin, NeverCacheMixin, View):
    """POST a room note; empty text deletes it."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            vnum = data["vnum"]
            text = data["text"]
        except (json.JSONDecodeError, KeyError, TypeError, UnicodeDecodeError):
            return JsonResponse({"error": "bad request"}, status=400)
        if not isinstance(vnum, int) or not isinstance(text, str):
            return JsonResponse({"error": "bad request"}, status=400)

        text = text.strip()[:NOTE_MAX_LENGTH]
        account_id = request.user.account_id

        if not text:
            RoomNote.objects.filter(
                account_id=account_id, room_vnum=vnum,
            ).delete()
            return JsonResponse({"ok": True, "text": ""})

        room = Room.objects.filter(vnum=vnum, is_deleted=False).first()
        if room is None:
            return JsonResponse({"error": "unknown room"}, status=404)
        RoomNote.objects.update_or_create(
            account_id=account_id,
            room_vnum=vnum,
            defaults={"zone_id": room.zone_id, "text": text},
        )
        return JsonResponse({"ok": True, "text": text})
