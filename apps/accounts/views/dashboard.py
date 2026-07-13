"""Eternal+ staff dashboard.

The game's weekly summary report (`run_weekly_summary_report`, ishar-mud
src/server/server.c) is clamped to Discord's message limits and only scratches
what the shared database can answer. This page is the first-class version —
the Discord post stays as the lite check-in. Everything here is a read of
tables the game already owns: live activity, the 7-day window, account
recency, the active-roster mix, the current season, and the
`historic_season_stat` snapshots from every cycled season. No game-side
dependency, no bridge, just the shared database.
"""
from datetime import timedelta

from django.db.models import Avg, Count, Max, Q, Sum
from django.utils.timezone import now
from django.views.generic.base import TemplateView

from apps.core.views.mixins import EternalRequiredMixin, NeverCacheMixin

from apps.accounts.models.account import Account
from apps.players.models.base import PlayerBase
from apps.players.models.game_type import GameType
from apps.players.models.player import Player
from apps.quests.models import PlayerQuest
from apps.seasons.models import HistoricSeasonStat
from apps.seasons.utils.current import get_current_season


# The end-game quests the game's weekly report singles out — keep in sync
# with the quest id list in `run_weekly_summary_report` (ishar-mud
# src/server/server.c).
ENDGAME_QUEST_IDS = (6, 7, 43, 52, 53)

# A season "participant" is an account with a character that got somewhere:
# reached this level or remorted. Filters out bot/throwaway registrations
# that rolled a character and never played it.
PARTICIPANT_MIN_LEVEL = 10

WEEK = timedelta(days=7)
MONTH = timedelta(days=30)


def _bars(counts):
    """[(label, n), …] -> bar rows with widths scaled to the largest value."""
    top = max((n for _, n in counts), default=0)
    return [
        {"label": label, "n": n, "pct": round(n / top * 100, 1) if top else 0}
        for label, n in counts
    ]


class DashboardView(EternalRequiredMixin, NeverCacheMixin, TemplateView):
    """Staff activity dashboard. Eternal+ (EternalRequiredMixin -> 404)."""

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current = now()
        week_ago = current - WEEK
        month_ago = current - MONTH
        season = get_current_season()
        context["season"] = season

        # Live now — the shared online queryset (logon/logout heuristic until
        # the game's presence heartbeat lands: isharmud/ishar-mud#1771).
        context["online_players"] = (
            Player.objects.online()
            .select_related("common")
            .order_by("-logon")
        )

        # This week: active mortals, grouped per account, most recent first.
        active_accounts = {}
        active_player_count = 0
        for player in (
            Player.objects.filter(logon__gte=week_ago)
            .select_related("account", "common")
            .order_by("-logon")
        ):
            entry = active_accounts.setdefault(
                player.account_id,
                {"account": player.account, "players": [], "last_logon": player.logon},
            )
            entry["players"].append(player)
            active_player_count += 1
        context["active_accounts"] = list(active_accounts.values())
        context["active_player_count"] = active_player_count
        context["total_accounts"] = Account.objects.count()

        # New players this week (all characters, matching the game report),
        # with play time and referrer.
        new_players = []
        for player in (
            PlayerBase.objects.filter(birth__gte=week_ago)
            .select_related("account", "account__referrer_account", "statistics")
            .order_by("-birth")
        ):
            stats = getattr(player, "statistics", None)
            new_players.append({
                "player": player,
                "hours": round((stats.total_play_time if stats else 0) / 3600, 1),
                "referrer": player.account.referrer_account,
            })
        context["new_players"] = new_players

        # Quest completions this week. End-game quests are the quests of
        # consequence, so the panel defaults to them; ?quests=all folds the
        # minor-quest noise back in.
        show_all_quests = self.request.GET.get("quests") == "all"
        quest_groups = {}
        for completion in (
            PlayerQuest.objects.filter(last_completed_at__gte=week_ago)
            .select_related("quest", "player")
            .order_by("player__name")
        ):
            group = quest_groups.setdefault(
                completion.quest_id,
                {
                    "quest": completion.quest,
                    "endgame": completion.quest_id in ENDGAME_QUEST_IDS,
                    "players": [],
                },
            )
            group["players"].append(completion.player)
        all_groups = sorted(
            quest_groups.values(),
            key=lambda g: (g["endgame"], len(g["players"])),
            reverse=True,
        )
        context["show_all_quests"] = show_all_quests
        context["quest_group_total"] = len(all_groups)
        context["quest_groups"] = (
            all_groups if show_all_quests
            else [g for g in all_groups if g["endgame"]]
        )
        context["endgame_completions"] = sum(
            len(g["players"]) for g in all_groups if g["endgame"]
        )

        # Season engagement funnel: of the accounts seen this season, how
        # recently was each one's latest character logon?
        season_lasts = (
            PlayerBase.objects.filter(logon__gte=season.effective_date)
            .values("account_id")
            .annotate(last=Max("logon"))
        )
        context["season_accounts"] = len(season_lasts)
        funnel = {"today": 0, "week": 0, "month": 0, "older": 0}
        for row in season_lasts:
            age = current - row["last"]
            if age <= timedelta(days=1):
                funnel["today"] += 1
            elif age <= WEEK:
                funnel["week"] += 1
            elif age <= MONTH:
                funnel["month"] += 1
            else:
                funnel["older"] += 1
        context["recency_bars"] = _bars((
            ("Today", funnel["today"]),
            ("This week", funnel["week"]),
            ("This month", funnel["month"]),
            ("Earlier this season", funnel["older"]),
        ))

        # Active-roster mix: mortals seen in the last 30 days, by class and
        # by game type.
        roster = (
            Player.objects.filter(logon__gte=month_ago)
            .select_related("common__player_class")
        )
        class_counts = {}
        type_counts = {}
        for player in roster:
            class_name = player.common.player_class.class_name.title()
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
            type_label = GameType(player.game_type).title
            type_counts[type_label] = type_counts.get(type_label, 0) + 1
        context["class_bars"] = _bars(
            sorted(class_counts.items(), key=lambda i: i[1], reverse=True)
        )
        context["type_bars"] = _bars(
            sorted(type_counts.items(), key=lambda i: i[1], reverse=True)
        )
        context["roster_count"] = len(roster)

        # Season-by-season history from the cycle-time snapshots, plus
        # cross-season retention: how many of a season's participants also
        # played the season before. The snapshot has a row for every player
        # that existed at cycle time — including bot/throwaway registrations
        # that never progressed — so only characters that got somewhere count.
        participated = HistoricSeasonStat.objects.filter(
            Q(level__gte=PARTICIPANT_MIN_LEVEL) | Q(remorts__gte=1)
        )
        participant_sets = {}
        for season_id, account_id in (
            participated.exclude(account_id=None)
            .values_list("season_id", "account_id")
            .distinct()
        ):
            participant_sets.setdefault(season_id, set()).add(account_id)

        history = []
        for row in (
            participated.values("season_id")
            .annotate(
                participants=Count("account_id", distinct=True),
                characters=Count("id"),
                avg_remorts=Avg("remorts"),
                max_remorts=Max("remorts"),
                play_time=Sum("play_time"),
            )
            .order_by("-season_id")
        ):
            mine = participant_sets.get(row["season_id"], set())
            prior = participant_sets.get(row["season_id"] - 1, set())
            history.append({
                **row,
                "hours": (row["play_time"] or 0) // 3600,
                "returning": len(mine & prior) if prior else None,
            })
        context["season_history"] = history
        context["participation_bars"] = _bars([
            (f"Season {row['season_id']}", row["participants"])
            for row in history
        ])
        return context
