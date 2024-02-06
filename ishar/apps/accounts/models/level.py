from django.db.models import IntegerChoices


class ImmortalLevel(IntegerChoices):
    """Immortal levels."""
    IMM_NONE = 0, "None"
    IMM_IMMORTAL = 1, "Immortal"
    IMM_ARTISAN = 2, "Artisan"
    IMM_ETERNAL = 3, "Eternal"
    IMM_FORGER = 4, "Forger"
    IMM_GOD = 5, "God"
