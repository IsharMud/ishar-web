from .forms import HelpSearchForm


def help_search_form(request):
    """Context processor for help topic search form."""
    return {"help_search_form": HelpSearchForm()}
