from django.db import models


class EventType(models.IntegerChoices):
    """Ishar global event type choices.

    Mirrors the game's `enum global_event_t` (ishar-mud constants.h) — the
    ordinals and display names must not drift. Types 10-13 are the automatic
    season-end countdown events: the game starts those itself as the season
    expiration approaches, so the events console offers to end but never to
    start them (`WEB_STARTABLE_EVENTS`).
    """

    BONUS_XP = 0, "Bonus Experience"
    TEST_SERVER = 1, "Test Server"
    CHALLENGE_XP = 2, "Challenge Experience"
    CHALLENGE_CYCLE_XP = 3, "Challenges Cycled"
    CRASH_XP = 4, "Crash Experience"
    WINTER_FEST = 5, "Festival of the Dancers"
    ST_PATRICK = 6, "Fortune's Convergence"
    JULY_FOURTH = 7, "July Fourth"
    HALLOWS_EVE = 8, "Veilfall"
    HARVEST_FEST = 9, "Harvest Fest"
    FOUR_WEEK_CYCLE = 10, "Rymaras' Echo"
    THREE_WEEK_CYCLE = 11, "The Comet's Wake"
    TWO_WEEK_CYCLE = 12, "Twilight of Titans"
    ONE_WEEK_CYCLE = 13, "Saorin's Reckoning"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self) -> str:
        return self.label


# Event types staff may start/extend from the web. The four season-end cycle
# events (10-13) are excluded: the game fires those automatically.
WEB_STARTABLE_EVENTS = tuple(e for e in EventType if e.value < 10)


class GlobalEvent(models.Model):
    """Ishar global Event."""

    event_type = models.IntegerField(
        primary_key=True,
        choices=EventType,
        help_text="Type of event.",
        verbose_name="Event Type",
    )
    start_time = models.DateTimeField(
        help_text="Date and time when the global event starts.",
        verbose_name="Start Time",
    )
    end_time = models.DateTimeField(
        help_text="Date and time when the global event ends.",
        verbose_name="End Time"
    )
    event_name = models.CharField(
        max_length=20,
        help_text="Internal name of the event.",
        verbose_name="Event Name",
    )
    event_desc = models.CharField(
        max_length=40,
        help_text="Friendly description of the event.",
        verbose_name="Event Description",
    )
    xp_bonus = models.IntegerField(
        help_text="Bonus experience (XP) percentage.",
        verbose_name="XP Bonus"
    )
    shop_bonus = models.IntegerField(
        help_text="Shop discount for items bought in-game during the event.",
        verbose_name="Shop Bonus",
    )
    celestial_luck = models.BooleanField(
        help_text="Boolean whether celestial luck applies during the event.",
        verbose_name="Celestial Luck",
    )

    class Meta:
        managed = False
        db_table = "global_event"
        default_related_name = "global_event"
        ordering = ("event_type",)
        verbose_name = "Global Event"
        verbose_name_plural = "Global Events"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {self.__str__()} ({self.event_type})"
        )

    def __str__(self) -> str:
        return self.event_desc
