from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from rest_framework import viewsets, permissions

from .models import Challenge
from .serializers import ChallengesSerializer


class ChallengesView(LoginRequiredMixin, ListView):
    """
    Challenges view.
    """
    context_object_name = "challenges"
    model = Challenge
    queryset = model.objects.filter(
        is_active__exact=1
    )
    template_name = "challenges.html.djt"


class CompleteChallengesView(ChallengesView):
    """
    Complete challenges view.
    """
    model = Challenge
    queryset = model.objects.filter(
        is_active__exact=1
    ).exclude(
        winner_desc__exact=""
    )


class IncompleteChallengesView(ChallengesView):
    """
    Complete challenges view.
    """
    model = Challenge
    queryset = model.objects.filter(
        is_active__exact=1,
        winner_desc__exact=""
    )


class ChallengesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows challenges to be viewed or edited.
    """
    model = Challenge
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = ChallengesSerializer
