from django import forms


class HelpSearchForm(forms.Form):
    search_topic = forms.CharField(help_text="", label="")
