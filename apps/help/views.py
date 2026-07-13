from difflib import get_close_matches

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from apps.skills.utils import find_skill_by_name

from .utils.helptab import get_helptab


class HelpView(TemplateView):
    """Help view."""

    template_name = "help_page.html"
    helptab = None
    help_topic = None
    help_topics = {}
    http_method_names = ("get", "post")
    status = 200
    suggestions = ()

    def setup(self, request, *args, **kwargs):
        # Re-parse the helptab on demand — it is a live mount from the game,
        # so get_helptab() serves the current file, not the parse pinned at
        # process start.
        self.helptab = get_helptab()
        self.help_topics = self.helptab.help_topics
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # Handle requests for search and specific help topic pages.

        # Get help topic name from URL, to search or find specific topic page.
        help_topic = kwargs.get("help_topic")
        if help_topic is not None:

            # Search the "helptab" file topic names and aliases for string.
            search_results = self.helptab.search(search_name=help_topic)

            # Handle any search results.
            if search_results:

                # Handle single result.
                if len(search_results) == 1:
                    search_result = next(iter(search_results.values()))

                    # Deprecated per-spell helptab entries are superseded by the
                    # live skill page: send "Spell X" topics to /skills/X/ when
                    # that skill exists, rather than render stale text.
                    if search_result.is_spell:
                        skill = find_skill_by_name(search_result.display_name)
                        if skill is not None:
                            return redirect(to=skill.get_absolute_url())

                    # Return exact name match directly.
                    if help_topic == search_result.name:
                        self.help_topic = search_result
                        return super().dispatch(request, *args, **kwargs)

                    # Redirect single result to that help topic page.
                    return redirect(to=search_result.get_absolute_url())

                # Set help topics to the search results.
                self.help_topics = search_results

            # No helptab topic matched. Mirror the game's `help` fallback
            # (ishar-mud src/dbase/help.c cmd_help): try a skill/spell name
            # next, then offer "did you mean" suggestions.
            else:
                skill = find_skill_by_name(help_topic)
                if skill is not None:
                    return redirect(to=skill.get_absolute_url())

                self.status = 404
                self.suggestions = self._suggest(help_topic)
                messages.error(
                    request=request,
                    message="Sorry, but no such help topic could be found.",
                )

        return super().dispatch(request, *args, **kwargs)

    def _suggest(self, query: str) -> list:
        # "Did you mean" for a 404: closest helptab topics *and* skill names,
        # each as a (label, url) pair so the template can route both kinds.
        q = (query or "").strip().casefold()
        if not q:
            return []

        pairs, seen = [], set()

        # Helptab topic suggestions (link to their help pages).
        for name in self.helptab.suggest(query, limit=6):
            topic = self.help_topics.get(name)
            if topic is not None and name not in seen:
                pairs.append((name, topic.get_absolute_url()))
                seen.add(name)

        # Skill-name suggestions (link to their skill pages) — the way
        # skill-only topics like "Earthquake" become findable from Help.
        # Restricted to mortal-visible skills so we never suggest a hidden one.
        from apps.skills.utils import visible_skills

        folded = {
            name.casefold(): name
            for name in visible_skills().values_list("skill_name", flat=True)
        }
        for match in get_close_matches(q, folded.keys(), n=6, cutoff=0.6):
            name = folded[match]
            if name not in seen:
                pairs.append((name, reverse("skill_page", args=(name,)) + "#skill"))
                seen.add(name)

        return pairs[:8]

    def get_context_data(self, **kwargs):
        # Include search form, help topics, and any chosen topic in context.
        context = super().get_context_data(**kwargs)
        context["help_topics"] = self.help_topics
        context["help_topic"] = self.help_topic
        context["suggestions"] = self.suggestions
        return context

    def render_to_response(self, context, **response_kwargs):
        # Return appropriate HTTP response status code.
        response_kwargs["status"] = self.status
        return super().render_to_response(context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        # Redirect HTTP POST request to GET (search) for the help topic string.
        return redirect(
            to="help_page",
            help_topic=request.POST.get("search_topic")
        )


class WorldView(TemplateView):
    """World (/world/) view."""

    template_name = "world.html"
    http_method_names = ("get",)

    def get_context_data(self, **kwargs):
        # Include sorted "areas" context of "Area " topics from "helptab" file.
        # Filter topics directly rather than via search() — the search ladder
        # optimizes for relevance, not "give me every Area topic".
        context = super().get_context_data(**kwargs)
        areas = [
            topic for topic in get_helptab().help_topics.values()
            if topic.is_area
        ]
        context["areas"] = sorted(areas)
        return context
