from rest_framework.serializers import ModelSerializer

from ishar.apps.faqs.models import FAQ


class FAQSerializer(ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"
