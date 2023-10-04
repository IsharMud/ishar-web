from rest_framework.serializers import ModelSerializer

from ishar.apps.races.models import Race, RaceAffinity, RaceDeathload, RaceSkill


class RaceSerializer(ModelSerializer):
    class Meta:
        model = Race
        fields = "__all__"


class RaceAffinitySerializer(ModelSerializer):
    class Meta:
        model = RaceAffinity
        fields = "__all__"


class RaceDeathloadSerializer(ModelSerializer):
    class Meta:
        model = RaceDeathload
        fields = "__all__"


class RaceSkillSerializer(ModelSerializer):
    class Meta:
        model = RaceSkill
        fields = "__all__"
