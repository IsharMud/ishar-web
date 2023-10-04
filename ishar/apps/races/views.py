from rest_framework import viewsets, permissions

from ishar.apps.races.models import Race, RaceAffinity, RaceDeathload, RaceSkill
from ishar.apps.races.serializers import (
    RaceSerializer, RaceAffinitySerializer, RaceDeathloadSerializer,
    RaceSkillSerializer
)


class RacesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows races to be viewed or edited.
    """
    model = Race
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = RaceSerializer


class RacesAffinityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows race affinities to be viewed or edited.
    """
    model = RaceAffinity
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = RaceAffinitySerializer


class RaceDeathloadViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows race deathloads to be viewed or edited.
    """
    model = RaceDeathload
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = RaceDeathloadSerializer


class RacesSkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows race's skills to be viewed or edited.
    """
    model = RaceSkill
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = RaceSkillSerializer
