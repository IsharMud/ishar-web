from rest_framework import viewsets, permissions

from ishar.apps.news.models import News
from ishar.apps.news.serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows news to be viewed or edited.
    """
    model = News
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = NewsSerializer
