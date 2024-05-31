from django.forms import Form, CharField, TextInput


class HelpSearchForm(Form):
    search_topic = CharField(
        help_text="",
        label="",
        widget=TextInput(
            attrs={'class': "rounded"}
        )
    )
