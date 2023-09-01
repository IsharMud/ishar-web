from rest_framework import serializers

from ..models import Force, Spell, SpellFlag


class ForceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Force
        fields = "__all__"


class SpellSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Spell
        fields = "__all__"


class SpellFlagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SpellFlag
        fields = "__all__"
