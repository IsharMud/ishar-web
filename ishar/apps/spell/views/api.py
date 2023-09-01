from rest_framework import viewsets, permissions

from ..models import Force, Spell, SpellFlag
from ..serializers import ForceSerializer, SpellSerializer, SpellFlagSerializer


class ForceAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows forces to be viewed or edited.
    """
    model = Force
    serializer_class = ForceSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()


class SpellAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows spells to be viewed or edited.
    """
    model = Spell
    serializer_class = SpellSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()


class SpellFlagAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows spell flags to be viewed or edited.
    """
    model = Spell
    serializer_class = SpellFlagSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
