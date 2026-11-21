from django.db import models

from apps.core.models.unsigned import UnsignedAutoField


class TrackScope(models.TextChoices):
    """`engagement_tracks.scope`. `standard` is the template a season runs
    when it has no track of its own; `upcoming` is staged for the next season
    and promoted to `season` by the game when it cycles."""

    STANDARD = "standard", "Standard template"
    SEASON = "season", "Season"
    UPCOMING = "upcoming", "Upcoming season"


class EngagementTrack(models.Model):
    """One engagement track document.

    Game-owned (rust-interop migration `create_engagement_tracks`) and
    read-only here: the game validates every change and holds the live track
    in memory, so the site enqueues `engagement_set_track` instead of writing
    this table. Contract: `docs/web_bridge_contracts.md` in ishar-mud.
    """

    track_id = UnsignedAutoField(primary_key=True)
    scope = models.CharField(max_length=8, choices=TrackScope)
    # 0 unless scope is `season`.
    season_id = models.PositiveIntegerField(default=0)
    milestones = models.JSONField(
        help_text=(
            '[{"slot", "at_bps", "rewards": [{"kind", "value", "count"?}]}],'
            " ascending by threshold. `slot` is the identity claim receipts"
            " reference."
        ),
    )
    updated_by = models.CharField(max_length=64)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "engagement_tracks"
        verbose_name = "Engagement Track"

    def __str__(self) -> str:
        if self.scope == TrackScope.SEASON:
            return f"Season {self.season_id} track"
        return self.get_scope_display()
