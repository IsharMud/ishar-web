from .forms import HelpSearchForm


def help_search_form(request):
    # Context processor for help topic search form.
    return {"HELP_SEARCH_FORM": HelpSearchForm()}
