from rest_framework.serializers import ModelSerializer

from ishar.apps.skills.models import (
    Force, SkillForce, Skill, SkillComponent, SkillSpellFlag, SpellFlag
)

class ForceSerializer(ModelSerializer):
    class Meta:
        model = Force
        fields = "__all__"


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class SpellFlagSerializer(ModelSerializer):
    class Meta:
        model = SpellFlag
        fields = "__all__"


class SkillComponentSerializer(ModelSerializer):
    model = SkillComponent
    fields = "__all__"


class SkillForceSerializer(ModelSerializer):
    class Meta:
        model = SkillForce
        fields = "__all__"


class SkillSpellFlagSerializer(ModelSerializer):
    class Meta:
        model = SkillSpellFlag
        fields = "__all__"
