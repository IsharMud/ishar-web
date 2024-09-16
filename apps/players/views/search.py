from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView

from ..forms import PlayerSearchForm
from ..models.player import Player


class PlayerSearchView(LoginRequiredMixin, FormView):
    """Player search view with form."""
    form_class = PlayerSearchForm
    model = Player
    status = 200
    template_name = "results.html"

    def form_valid(self, form):
        """Process valid form."""
        context = self.get_context_data()
        if form.cleaned_data:
            search = form.cleaned_data.get("name")
            if search:
                results = self.model.objects.filter(
                    name__icontains=search,
                    account__is_private__exact=False
                ).order_by(
                    "name"
                )

                # Count any results.
                if results:
                    num_results = results.count()

                    # Redirect directly to a single match.
                    if num_results == 1:
                        who = results.first()
                        return redirect(who.get_absolute_url())

                    # Otherwise, include results and search term in context.
                    if num_results > 1:
                        context["results"] = results
                        context["search"] = search

                else:
                    self.status = 404
                    messages.add_message(
                        request=self.request,
                        level=messages.ERROR,
                        message="Sorry, but no such player could be found."
                    )

        return self.render_to_response(context=context, status=self.status)
