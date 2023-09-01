from rest_framework import viewsets, permissions

from ..models import News
from ..serializers import NewsSerializer


class NewsAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows news to be viewed or edited.
    """
    model = News
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = News.objects.all()
