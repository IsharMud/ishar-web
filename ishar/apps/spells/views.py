from rest_framework import viewsets, permissions

from .models import Force, Spell, SpellFlag, SpellSpellFlag
from .serializers import ForceSerializer, SpellSerializer, \
    SpellFlagSerializer, SpellSpellFlagSerializer


class ForcesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows forces to be viewed or edited.
    """
    model = Force
    serializer_class = ForceSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()


class SpellsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows spells to be viewed or edited.
    """
    model = Spell
    serializer_class = SpellSerializer
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


class SpellsFlagsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows spell's flags to be viewed or edited.
    """
    model = SpellSpellFlag
    serializer_class = SpellSpellFlagSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
