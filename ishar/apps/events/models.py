from django.db import models


class GlobalEvent(models.Model):
    """
    Global Event.
    """
    event_type = models.IntegerField(
        primary_key=True,
        choices=(
            (0, "BONUS_XP [0]"),
            (1, "TEST_SERVER [1]"),
            (2, "CHALLENGE_XP [2]"),
            (3, "CHALLENGE_CYCLE_XP [3]"),
            (4, "CRASH_XP [4]"),
            (5, "WINTER_FEST [5]"),
            (6, "ST_PATRICK [6]"),
            (7, "JULY_FOURTH [7]"),
            (8, "HALLOWS_EVE [8]"),
            (9, "HARVEST_FEST [9]"),
            (10, "MAX_EVENT [10]")
        ),
        help_text="Type of event.",
        verbose_name="Event Type",
    )
    start_time = models.DateTimeField(
        help_text="Date and time when the global event starts.",
        verbose_name="Start Time"
    )
    end_time = models.DateTimeField(
        help_text="Date and time when the global event ends.",
        verbose_name="End Time"
    )
    event_name = models.CharField(
        max_length=20,
        help_text="Internal name of the event.",
        verbose_name="Event Name"
    )
    event_desc = models.CharField(
        max_length=40,
        help_text="Friendly description of the event.",
        verbose_name="Event Description"
    )
    xp_bonus = models.IntegerField(
        help_text="Bonus experience (XP) percentage.",
        verbose_name="XP Bonus"
    )
    shop_bonus = models.IntegerField(
        help_text="Shop discount for items bought in-game during the event.",
        verbose_name="Shop Bonus"
    )
    celestial_luck = models.BooleanField(
        help_text="Boolean whether celestial luck applies during the event.",
        verbose_name="Celestial Luck"
    )

    class Meta:
        managed = False
        db_table = "global_event"
        default_related_name = "global_event"
        ordering = ("event_type",)
        verbose_name = "Global Event"
        verbose_name_plural = "Global Events"

    def __repr__(self):
        return "%s: %s (%s)" % (
            self.__class__.__name__,
            self.__str__(),
            self.event_type
        )

    def __str__(self):
        return self.event_desc
