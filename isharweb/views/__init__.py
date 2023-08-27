"""
isharmud.com views.
"""
from django.views.generic.base import TemplateView


class WelcomeView(TemplateView):
    """
    Main isharmud.com welcome view.
    """
    template_name = 'welcome.html.djt'

