from django.contrib import admin

from .models import Race, RaceAffinity, RaceSkill



@admin.register(RaceAffinity)
class RaceAffinitiesAdmin(admin.ModelAdmin):
    """
    Ishar race affinity administration.
    """
    model = RaceAffinity
    fieldsets = (
        (None, {"fields": ("race_affinity_id",)}),
        ("Race", {"fields": ("race",)}),
        ("Force", {"fields": ("force",)}),
        ("Affinity", {"fields": ("affinity_type",)})
    )
    list_display = ("race_affinity_id", "race", "force", "affinity_type")
    list_filter = (
        "affinity_type",
        ("force", admin.RelatedOnlyFieldListFilter),
        ("race", admin.RelatedOnlyFieldListFilter),
    )
    readonly_fields = ("race_affinity_id",)
    search_fields = ("race", "force", "affinity_type")

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False


class RaceAffinityAdminInline(admin.TabularInline):
    """
    Ishar race affinity inline administration.
    """
    extra = 1
    model = RaceAffinity

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False


class RaceSkillAdminInline(admin.TabularInline):
    """
    Ishar race skill inline administration.
    """
    extra = 1
    model = RaceSkill

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False


@admin.register(Race)
class RacesAdmin(admin.ModelAdmin):
    """
    Ishar race administration.
    """
    model = Race
    fieldsets = (
        (None, {"fields": ("race_id", "display_name", "symbol", "folk_name")}),
        ("Descriptions", {"fields": ("short_description", "long_description")}),
        ("Defaults", {"fields": (
            "default_movement", "default_height", "default_weight"
        )}),
        ("Bonus", {"fields": (
            "bonus_fortitude", "bonus_reflex", "bonus_resilience",
            "listen_sound", "height_bonus", "weight_bonus"
        )}),
        ("Attacks", {"fields": ("attack_noun", "attack_type")}),
        ("Weaknesses", {"fields": ("vulnerabilities", "susceptibilities")}),
        ("Protections", {"fields": ("resistances", "immunities")}),
        ("Additional Statistics", {"fields": (
            "additional_str", "additional_agi", "additional_end",
            "additional_per", "additional_foc", "additional_wil"
        )}),
        ("Booleans", {"fields": (
            "is_humanoid", "is_invertebrae", "is_flying", "is_swimming",
            "darkvision", "see_invis", "is_walking",
            "endure_heat", "endure_cold", "is_undead", "is_playable"
        )}),
    )
    inlines = (RaceSkillAdminInline, RaceAffinityAdminInline)
    list_display = (
        "display_name", "symbol", "is_playable", "folk_name",
        "short_description"
    )
    list_filter = ("is_playable",)
    readonly_fields = ("race_id",)
    search_fields = (
        "display_name", "symbol", "folk_name", "attack_noun",
        "short_description", "long_description"
    )

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_immortal()
        return False
