from rest_framework.serializers import ModelSerializer

from .models import Force, Skill, SpellFlag, SkillSpellFlag


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


class SkillSpellFlagSerializer(ModelSerializer):
    class Meta:
        model = SkillSpellFlag
        fields = "__all__"
