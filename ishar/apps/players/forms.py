from django.forms import Form, SlugField, TextInput


class PlayerSearchForm(Form):
    """Form with single text input for searching player name."""
    name = SlugField(
        help_text="",
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control form-control-md",
                "aria-label": "Player Name",
                "placeholder": "Player Name",
            }
        )
    )
