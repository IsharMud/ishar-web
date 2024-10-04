from django.forms import Form, CharField, TextInput


class HelpSearchForm(Form):
    """Form with single text input for searching help topic names."""

    search_topic = CharField(
        help_text="",
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control rounded",
                "aria-label": "Topic Name",
                "placeholder": "Topic Name",
            }
        )
    )
