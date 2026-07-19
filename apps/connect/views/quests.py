"""JSON endpoints for the HUD Quest Log (isharmud/ishar-web#150).

The quest data model splits like the map's: GMCP ``Char.Quests`` carries
per-player *dynamic* state (status, step progress), while the *static*
catalog — descriptions, intros, step labels, reward names — is served
here from the game's authoritative tables, ETagged and cached like the
zone graph. The split is part of the GMCP contract
(``ishar-mud docs/gmcp_feeds.md``, Char.Quests information policy).

Two rules from that contract are enforced here, not just upstream:

* Mystified steps serve only ``mystify_text`` — never the real target.
* ``quest_source`` / ``quest_return`` are omitted entirely: quest-giver
  locations reach the client only via the per-viewer-filtered
  ``Room.QuestMarkers`` feed.

``QuestTrackedView`` / ``QuestTrackView`` are the account's tracked-quest
set (pin-to-top + objectives tracker), following the map fog-of-war
state conventions.
"""
import hashlib
import json

from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View

from apps.core.views.mixins import NeverCacheMixin
from apps.mobiles.models import Mobile
from apps.objects.models.object import Object
from apps.players.models.remort_upgrade import RemortUpgrade
from apps.quests.models import Quest
from apps.quests.models.prereq import QuestPrereq
from apps.quests.models.recipe import ProfessionRecipe
from apps.quests.models.reward import QuestReward
from apps.quests.models.step import QuestStep
from apps.rooms.models import Room
from apps.skills.models.skill import Skill

from ..models import QuestTrack
from .map import MapJSONMixin, strip_color


TRACK_MAX = 8

# quest_steps.step_type (game enum order: constants.h).
STEP_OBJECT, STEP_KILL, STEP_ROOM, STEP_DIALOGUE, STEP_SPECIAL, STEP_ESCORT = (
    range(6)
)

STEP_LABEL_PREFIX = {
    STEP_OBJECT: "Retrieve - ",
    STEP_KILL: "Kill - ",
    STEP_ROOM: "Find - ",
    STEP_ESCORT: "Escort to - ",
}

# quest_rewards.reward_type (game enum order: constants.h).
(
    REWARD_OBJ_ALWAYS, REWARD_OBJ_CHOICE, REWARD_CASH, REWARD_ALIGN,
    REWARD_SKILL, REWARD_RENOWN, REWARD_XP, REWARD_QUEST, REWARD_HEIRLOOM,
    REWARD_BUFF, REWARD_UPGRADE, REWARD_MEMORY, REWARD_RECIPE,
) = range(13)


class QuestCatalogView(MapJSONMixin, View):
    """GET the static quest catalog: every quest's display fields, step
    labels, and reward names. Per-player state rides GMCP; the client
    joins the two on quest id."""

    http_method_names = ("get",)

    def get(self, request, *args, **kwargs):
        quests = list(
            Quest.objects.values(
                "quest_id", "display_name", "description", "quest_intro",
                "min_level", "repeatable", "class_restrict",
            )
        )
        steps = list(
            QuestStep.objects.values(
                "quest_id", "step_type", "target", "num_required",
                "mystify", "mystify_text",
            ).order_by("step_id")
        )
        rewards = list(
            QuestReward.objects.values(
                "quest_id", "reward_type", "reward_num", "class_restrict",
            ).order_by("quest_reward_id")
        )
        prereqs = list(
            QuestPrereq.objects.values("quest_id", "required_quest")
        )

        # Bulk-resolve step targets and reward objects to display names,
        # mirroring the game's objective labels (quest_step_objective_label).
        mob_vnums, obj_vnums, room_vnums = set(), set(), set()
        skill_ids, recipe_ids, upgrade_ids = set(), set(), set()
        for s in steps:
            if s["mystify"]:
                continue
            if s["step_type"] == STEP_OBJECT:
                obj_vnums.add(s["target"])
            elif s["step_type"] == STEP_KILL:
                mob_vnums.add(s["target"])
            elif s["step_type"] in (STEP_ROOM, STEP_ESCORT):
                room_vnums.add(s["target"])
        for r in rewards:
            if r["reward_type"] in (
                REWARD_OBJ_ALWAYS, REWARD_OBJ_CHOICE, REWARD_HEIRLOOM,
                REWARD_MEMORY,
            ):
                obj_vnums.add(r["reward_num"])
            elif r["reward_type"] == REWARD_SKILL:
                skill_ids.add(r["reward_num"])
            elif r["reward_type"] == REWARD_RECIPE:
                recipe_ids.add(r["reward_num"])
            elif r["reward_type"] == REWARD_UPGRADE:
                upgrade_ids.add(r["reward_num"])

        mob_names = {
            m["id"]: strip_color(m["long_name"] or m["name"])
            for m in Mobile.objects.filter(id__in=mob_vnums).values(
                "id", "name", "long_name",
            )
        }
        obj_names = {
            o["vnum"]: strip_color(o["longname"] or o["name"])
            for o in Object.objects.filter(vnum__in=obj_vnums).values(
                "vnum", "name", "longname",
            )
        }
        room_names = {
            r["vnum"]: strip_color(r["name"])
            for r in Room.objects.filter(
                vnum__in=room_vnums, is_deleted=False,
            ).values("vnum", "name")
        }
        skill_names = {
            s["id"]: s["skill_name"]
            for s in Skill.objects.filter(id__in=skill_ids).values(
                "id", "skill_name",
            )
        }
        recipe_names = {
            r["id"]: r["name"]
            for r in ProfessionRecipe.objects.filter(id__in=recipe_ids).values(
                "id", "name",
            )
        }
        upgrade_names = {
            u["upgrade_id"]: u["display_name"] or u["name"]
            for u in RemortUpgrade.objects.filter(
                upgrade_id__in=upgrade_ids,
            ).values("upgrade_id", "name", "display_name")
        }
        quest_names = {q["quest_id"]: q["display_name"] for q in quests}

        def step_label(s):
            if s["mystify"]:
                return s["mystify_text"] or "A hidden objective"
            prefix = STEP_LABEL_PREFIX.get(s["step_type"])
            if s["step_type"] == STEP_OBJECT:
                name = obj_names.get(s["target"])
            elif s["step_type"] == STEP_KILL:
                name = mob_names.get(s["target"])
            elif s["step_type"] in (STEP_ROOM, STEP_ESCORT):
                name = room_names.get(s["target"])
            else:
                return "A special objective"
            if prefix is None or name is None:
                return "A special objective"
            return prefix + name

        def reward_entry(r):
            t, n = r["reward_type"], r["reward_num"]
            if t in (REWARD_OBJ_ALWAYS, REWARD_OBJ_CHOICE):
                name = obj_names.get(n)
                if name is None:
                    return None
                return {
                    "kind": "item" if t == REWARD_OBJ_ALWAYS else "choice",
                    "name": name,
                }
            if t == REWARD_CASH:
                return {"kind": "cash", "name": f"{n} Obsidian"}
            if t == REWARD_ALIGN:
                return {"kind": "align", "name": f"{n} Alignment"}
            if t == REWARD_SKILL:
                name = skill_names.get(n)
                return {"kind": "skill", "name": name} if name else None
            if t == REWARD_XP:
                return {"kind": "xp", "name": f"{n} Experience"}
            if t == REWARD_QUEST:
                name = quest_names.get(n)
                return {"kind": "quest", "name": name} if name else None
            if t == REWARD_HEIRLOOM:
                name = obj_names.get(n)
                return {"kind": "relic", "name": name} if name else None
            if t == REWARD_MEMORY:
                name = obj_names.get(n)
                return {"kind": "memory", "name": name} if name else None
            if t == REWARD_RECIPE:
                name = recipe_names.get(n)
                return {"kind": "recipe", "name": "Recipe: " + name} if name else None
            if t == REWARD_UPGRADE:
                name = upgrade_names.get(n)
                return {"kind": "upgrade", "name": name} if name else None
            # Renown is unadvertised in-game (the display switch skips it);
            # buff rewards are unused in current content.
            return None

        steps_by_quest, rewards_by_quest, prereqs_by_quest = {}, {}, {}
        for s in steps:
            steps_by_quest.setdefault(s["quest_id"], []).append({
                "label": step_label(s),
                "need": s["num_required"],
                **({"mystify": True} if s["mystify"] else {}),
            })
        for r in rewards:
            entry = reward_entry(r)
            if entry is None:
                continue
            if r["class_restrict"] >= 0:
                entry["class_restrict"] = r["class_restrict"]
            rewards_by_quest.setdefault(r["quest_id"], []).append(entry)
        for p in prereqs:
            prereqs_by_quest.setdefault(p["quest_id"], []).append(
                p["required_quest"]
            )

        payload = {
            "quests": [
                {
                    "id": q["quest_id"],
                    "name": q["display_name"],
                    "desc": strip_color(q["description"] or ""),
                    "intro": strip_color(q["quest_intro"] or ""),
                    "min_level": q["min_level"],
                    **({"repeatable": True} if q["repeatable"] else {}),
                    **(
                        {"class_restrict": q["class_restrict"]}
                        if q["class_restrict"] >= 0
                        else {}
                    ),
                    **(
                        {"prereqs": prereqs_by_quest[q["quest_id"]]}
                        if q["quest_id"] in prereqs_by_quest
                        else {}
                    ),
                    "steps": steps_by_quest.get(q["quest_id"], []),
                    "rewards": rewards_by_quest.get(q["quest_id"], []),
                }
                for q in quests
            ]
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


class QuestTrackedView(MapJSONMixin, NeverCacheMixin, View):
    """GET the account's tracked quest ids."""

    http_method_names = ("get",)

    def get(self, request, *args, **kwargs):
        tracked = list(
            QuestTrack.objects.filter(
                account_id=request.user.account_id,
            ).order_by("created_at").values_list("quest_id", flat=True)
        )
        return JsonResponse({"tracked": tracked, "max": TRACK_MAX})


class QuestTrackView(MapJSONMixin, NeverCacheMixin, View):
    """POST {quest_id, on} to track/untrack a quest (cap TRACK_MAX)."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            quest_id = data["quest_id"]
            on = data["on"]
        except (json.JSONDecodeError, KeyError, TypeError, UnicodeDecodeError):
            return JsonResponse({"error": "bad request"}, status=400)
        if (
            not isinstance(quest_id, int) or isinstance(quest_id, bool)
            or not isinstance(on, bool) or not 0 <= quest_id < 10**6
        ):
            return JsonResponse({"error": "bad request"}, status=400)

        account_id = request.user.account_id
        if not on:
            QuestTrack.objects.filter(
                account_id=account_id, quest_id=quest_id,
            ).delete()
        else:
            if not Quest.objects.filter(quest_id=quest_id).exists():
                return JsonResponse({"error": "unknown quest"}, status=404)
            if (
                QuestTrack.objects.filter(account_id=account_id)
                .exclude(quest_id=quest_id).count() >= TRACK_MAX
            ):
                return JsonResponse({"error": "track limit"}, status=409)
            QuestTrack.objects.get_or_create(
                account_id=account_id, quest_id=quest_id,
            )

        tracked = list(
            QuestTrack.objects.filter(account_id=account_id)
            .order_by("created_at").values_list("quest_id", flat=True)
        )
        return JsonResponse({"ok": True, "tracked": tracked, "max": TRACK_MAX})
