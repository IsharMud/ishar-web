from django.views.generic.base import TemplateView


class InteractionsView(TemplateView):
    """
    Interactions view.
    """
    template_name = "interactions.html"
    http_method_names = ("get", "post")
    status = 200

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            context=self.get_context_data(**kwargs),
            status=self.status
        )

    def post(self, request, *args, **kwargs):
        return self.render_to_response(
            context=self.get_context_data(**kwargs),
            status=self.status
        )
