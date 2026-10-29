from collections import OrderedDict
from dataclasses import dataclass, field

from django.db.models import Prefetch
from django.views.generic.base import TemplateView

from apps.accounts.models import AccountAchievement
from apps.core.models.title import Title
from apps.core.views.mixins import NeverCacheMixin
from apps.objects.models.object import Object

from ..models.achievement import Achievement
from ..models.criteria import AchievementCriteria
from ..models.reward import AchievementReward, AchievementRewardType


@dataclass
class Reward:
    kind: str          # "points" | "essence" | "title" | "item"
    label: str
    css: str           # .ac-pill modifier


@dataclass
class Row:
    achievement: Achievement
    points: int = 0
    rewards: list = field(default_factory=list)
    criteria: list = field(default_factory=list)
    done: bool = False
    completed_at=None
    completed_by: str = ""


@dataclass
class Group:
    category: str
    sub: str
    rows: list = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.category} · {self.sub}" if self.sub else self.category

    @property
    def anchor(self) -> str:
        return (self.category + ("-" + self.sub if self.sub else "")).lower()

    @property
    def done(self) -> int:
        return sum(1 for r in self.rows if r.done)


class AchievementsView(NeverCacheMixin, TemplateView):
    """The achievement catalog, grouped as the in-game ``achievement`` command
    groups it (category, then ``parent_category`` — which, despite its name,
    is the sub-category). A hidden achievement is not shown to a viewer who
    has not earned it; completion comes from ``account_achievements`` when the
    viewer is logged in."""

    template_name = "achievements.html"
    http_method_names = ("get",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        earned = {}
        if user.is_authenticated:
            earned = {
                row.achievement_id: row
                for row in AccountAchievement.objects.filter(
                    account=user, is_completed=1,
                )
            }

        achievements = (
            Achievement.objects.all()
            .prefetch_related(
                Prefetch("reward", queryset=AchievementReward.objects.all()),
                Prefetch("criteria", queryset=AchievementCriteria.objects.order_by("group_id", "criteria_id")),
            )
            .order_by("category", "parent_category", "ordinal", "created_at")
        )
        # Nulls sort first in the game (no sub-category before any named one);
        #   MariaDB and sqlite already order NULL first ascending.

        titles = {t.pk: t for t in Title.objects.all()}
        item_ids = {
            r.reward_value
            for a in achievements for r in a.reward.all()
            if r.reward_type == AchievementRewardType.SOULBOUND_ITEM
        }
        items = {o.pk: o for o in Object.objects.filter(pk__in=item_ids)} if item_ids else {}

        groups = OrderedDict()
        shown = total = done_count = points_total = 0
        for achievement in achievements:
            total += 1
            completion = earned.get(achievement.pk)
            if achievement.is_hidden and completion is None:
                continue
            row = Row(achievement=achievement)
            for reward in achievement.reward.all():
                built = self.build_reward(reward, titles, items)
                if built is None:
                    continue
                if built.kind == "points":
                    row.points += reward.reward_value or 0
                else:
                    row.rewards.append(built)
            row.criteria = [
                c.description for c in achievement.criteria.all() if c.description
            ]
            if completion is not None:
                row.done = True
                row.completed_at = completion.completion_date
                row.completed_by = completion.completed_by or ""
                done_count += 1
                points_total += row.points
            shown += 1
            key = (achievement.category or "", achievement.parent_category or "")
            if key not in groups:
                groups[key] = Group(category=key[0] or "General", sub=key[1])
            groups[key].rows.append(row)

        context.update({
            "groups": list(groups.values()),
            "shown": shown,
            "total": total,
            "done_count": done_count,
            "points_total": points_total,
            "hidden_exist": shown < total,
            "viewer": user if user.is_authenticated else None,
        })
        return context

    @staticmethod
    def build_reward(reward, titles, items):
        kind = reward.reward_type
        value = reward.reward_value or 0
        if kind == AchievementRewardType.ACHIEVEMENT_POINTS:
            return Reward(kind="points", label=f"{value} pts", css="accent")
        if kind == AchievementRewardType.ESSENCE:
            return Reward(kind="essence", label=f"{value} essence", css="ok")
        if kind == AchievementRewardType.TITLE:
            title = titles.get(value)
            if title is None:
                return None
            # The game picks the form by the character's sex; an account has
            #   characters of either, so show both when they differ.
            forms = [t for t in (title.male_text, title.female_text) if t]
            label = " / ".join(dict.fromkeys(forms)) or "a title"
            return Reward(kind="title", label=f"title: {label}", css="info")
        if kind == AchievementRewardType.SOULBOUND_ITEM:
            item = items.get(value)
            name = (item.longname or item.name) if item else "a soulbound item"
            return Reward(kind="item", label=name, css="warn")
        return None
