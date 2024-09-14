from django.forms import Form, CharField, TextInput


class HelpSearchForm(Form):
    """Search text input for finding help topics."""
    search_topic = CharField(
        help_text="",
        label="",
        widget=TextInput(
            attrs={
                "class": "rounded",
                "placeholder": "Topic Name"
            }
        )
    )
