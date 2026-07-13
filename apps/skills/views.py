from difflib import get_close_matches

from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from apps.classes.models.skill import ClassSkill
from apps.races.models.skill import RaceSkill

from .models import Skill
from .utils import find_skill_by_name, visible_skills


class SkillIndexView(TemplateView):
    """Public, searchable index of every skill/spell, grouped by class."""

    template_name = "skills.html"
    http_method_names = ("get",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # The set of skills a mortal is allowed to see: Skill/Spell/Passive,
        # learnable by a playable class or race, not season-gated.
        visible_ids = set(visible_skills().values_list("id", flat=True))

        # Group them under each playable class, ordered by learn level, using
        # only non-deprecated class rows (min_level >= 0, max_learn > 0) so the
        # game's hidden/deprecated skills stay out of the lists.
        class_skills = (
            ClassSkill.objects
            .select_related("skill", "player_class")
            .filter(
                player_class__is_playable=True,
                min_level__gte=0,
                max_learn__gt=0,
                skill_id__in=visible_ids,
            )
            .order_by("player_class__class_name", "min_level", "skill__skill_name")
        )
        groups: dict = {}
        shown_ids: set = set()
        for class_skill in class_skills:
            group = groups.setdefault(
                class_skill.player_class_id,
                {
                    "id": f"class-{class_skill.player_class_id}",
                    "name": str(class_skill.player_class),
                    "skills": [],
                },
            )
            group["skills"].append(
                {"skill": class_skill.skill, "level": class_skill.min_level}
            )
            shown_ids.add(class_skill.skill_id)

        class_groups = sorted(groups.values(), key=lambda g: g["name"].lower())

        # A "Racial" bucket for skills a *playable* race grants but no playable
        # class does, so racial abilities are still discoverable by browsing.
        # Non-playable (immortal / mob-only) races are excluded, matching the
        # mortal view of the game.
        racial_ids = (
            set(
                RaceSkill.objects
                .filter(
                    race__is_playable=True, level__gte=0, skill_id__in=visible_ids,
                )
                .values_list("skill_id", flat=True)
            )
            - shown_ids
        )
        racial_skills = list(
            Skill.objects.filter(id__in=racial_ids).order_by("skill_name")
        )
        if racial_skills:
            class_groups.append(
                {
                    "id": "racial",
                    "name": "Racial",
                    "skills": [{"skill": s, "level": None} for s in racial_skills],
                }
            )
            shown_ids.update(s.id for s in racial_skills)

        context["groups"] = class_groups
        context["skill_count"] = len(shown_ids)
        return context


class SkillDetailView(TemplateView):
    """Public page for one skill/spell, mirroring the in-game ``skill``
    command (``display_skill_full``) minus per-player state."""

    template_name = "skill_page.html"
    http_method_names = ("get",)
    skill = None
    status = 200
    query = ""
    suggestions = ()

    def dispatch(self, request, *args, **kwargs):
        name = (kwargs.get("skill_name") or "").strip()
        skill = find_skill_by_name(name)

        if skill is None:
            # No match: 404 with "did you mean" from the closest skill names.
            self.status = 404
            self.query = name
            self.suggestions = self._suggest(name)
        elif skill.skill_name != name:
            # Case difference or abbreviation: send to the canonical URL.
            return redirect(skill.get_absolute_url())
        else:
            self.skill = skill

        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def _suggest(name: str) -> list:
        if not name:
            return []
        names = visible_skills().values_list("skill_name", flat=True)
        folded = {n.casefold(): n for n in names}
        return [
            folded[match]
            for match in get_close_matches(
                name.casefold(), folded.keys(), n=6, cutoff=0.6
            )
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["skill"] = self.skill
        context["query"] = self.query
        context["suggestions"] = self.suggestions

        if self.skill is not None:
            # Only playable classes/races that can actually learn it, mirroring
            # display_skill_full's mortal view: it hides non-playable (immortal
            # / mob-only) classes/races and deprecated rows (can_learn == -1,
            # i.e. min_level < 0 or max_learn <= 0).
            context["class_skills"] = (
                ClassSkill.objects
                .filter(
                    skill=self.skill, player_class__is_playable=True,
                    min_level__gte=0, max_learn__gt=0,
                )
                .select_related("player_class")
                .order_by("min_level", "player_class__class_name")
            )
            context["race_skills"] = (
                RaceSkill.objects
                .filter(skill=self.skill, race__is_playable=True, level__gte=0)
                .select_related("race")
                .order_by("level", "race__display_name")
            )
            context["forces"] = [
                skill_force.force
                for skill_force in self.skill.forces.select_related("force")
            ]
            context["components"] = list(self.skill.components.all())

            # Facts that need get_FOO_display() or safe FK handling are resolved
            # here so the template stays presentational.
            skill = self.skill
            context["min_posn_display"] = (
                skill.get_min_posn_display()
                if skill.min_posn is not None and skill.min_posn > 0
                else ""
            )
            context["save_display"] = (
                skill.get_req_save_display()
                if skill.req_save is not None and skill.req_save >= 0
                else ""
            )
            parent_id = skill.parent_skill_id or -1
            context["parent_skill"] = (
                Skill.objects.filter(id=parent_id).first() if parent_id > 0 else None
            )
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs["status"] = self.status
        return super().render_to_response(context, **response_kwargs)
