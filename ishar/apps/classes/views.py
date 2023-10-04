from rest_framework import viewsets, permissions

from ishar.apps.classes.models import Class
from ishar.apps.classes.serializers import ClassSerializer


class ClassesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows classes to be viewed or edited.
    """
    model = Class
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = ClassSerializer
