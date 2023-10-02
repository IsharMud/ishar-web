from rest_framework import viewsets, permissions

from ishar.apps.skills.models import Force, Skill, SpellFlag, SkillSpellFlag
from ishar.apps.skills.serializers import (
    ForceSerializer, SkillSerializer, SpellFlagSerializer,
    SkillSpellFlagSerializer
)


class ForcesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows forces to be viewed or edited.
    """
    model = Force
    serializer_class = ForceSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()


class SkillsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows spells to be viewed or edited.
    """
    model = Skill
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()


class SkillsFlagsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows skill/spell's flags to be viewed or edited.
    """
    model = SkillSpellFlag
    serializer_class = SkillSpellFlagSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()


class SpellFlagsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows spell flags to be viewed or edited.
    """
    model = SpellFlag
    serializer_class = SpellFlagSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
