from rest_framework.serializers import ModelSerializer

from ..models import Force, Spell, SpellFlag


class ForceSerializer(ModelSerializer):
    class Meta:
        model = Force
        fields = "__all__"


class SpellSerializer(ModelSerializer):
    class Meta:
        model = Spell
        fields = "__all__"


class SpellFlagSerializer(ModelSerializer):
    class Meta:
        model = SpellFlag
        fields = "__all__"
