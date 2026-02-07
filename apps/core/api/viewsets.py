from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet


class BaseAPIModelViewSet(ReadOnlyModelViewSet):
    """
    Base read-only Django-Rest-Framework (DRF) API view-set.
    """
    fields = filterset_fields = "__all__"
    model = None
    permission_classes = IsAdminUser
    serializer_class = None

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
