from django.contrib.admin import site

from ..models.challenge import Challenge
from .challenge import ChallengeAdmin


site.register(Challenge, ChallengeAdmin)
