from django.forms import Form, SlugField, TextInput


class PlayerSearchForm(Form):
    """Form with single text input for searching player names."""

    name = SlugField(
        help_text="",
        label="",
        widget=TextInput(
            attrs={
                "class": "ac-input",
                "aria-label": "Player Name",
                "placeholder": "Player Name",
            }
        ),
    )
