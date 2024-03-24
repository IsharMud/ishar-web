from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView

from ..forms.search import PlayerSearchForm
from ..models.player import Player


class PlayerSearchView(LoginRequiredMixin, FormView):
    """Player search view with form."""
    form_class = PlayerSearchForm
    model = Player
    template_name = "search.html"

    def form_valid(self, form):
        """Process valid form."""
        context = self.get_context_data()
        if form.cleaned_data:
            search = form.cleaned_data.get("name")
            if search:
                results = self.model.objects.filter(name__icontains=search)

                # Count any results.
                if results:
                    num_results = results.count()

                    # Redirect directly to a single match.
                    if num_results == 1:
                        return redirect(results.first().get_absolute_url())

                    # Otherwise, include results and search term in context.
                    if num_results > 1:
                        context["results"] = results
                        context["search"] = search

        return self.render_to_response(context=context)

    def get_form(self, form_class=None):
        """Remove help text and label from player name search form."""
        form = super().get_form(form_class=form_class)
        form["name"].help_text = form["name"].label = ''
        return form
