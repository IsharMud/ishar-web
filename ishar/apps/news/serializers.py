from rest_framework.serializers import ModelSerializer

from ishar.apps.news.models import News


class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"
