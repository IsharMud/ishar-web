from django.forms.models import ModelForm

from ..models.player import Player


class PlayerSearchForm(ModelForm):
    class Meta:
        model = Player
        fields = ("name",)
