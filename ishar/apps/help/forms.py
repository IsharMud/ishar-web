from django.forms import Form, CharField


class HelpSearchForm(Form):
    search_topic = CharField(help_text="", label="")
