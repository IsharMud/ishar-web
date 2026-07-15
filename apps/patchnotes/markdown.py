"""
Render a patch note's lightweight markdown to safe HTML.

The game stores patch-note bodies in a tiny markdown subset and renders them to
ANSI for telnet in `patch_notes.rs::render_body_for_telnet`. This is the web
mirror of that exact subset, so a note reads the same in the browser as in-game:

- ``## Heading``      -> ``<h3>``
- ``- bullet``        -> ``<li>`` (consecutive bullets grouped in one ``<ul>``)
- ``**bold**``        -> ``<strong>`` (inline, anywhere on a line)
- blank line          -> paragraph break
- anything else       -> ``<p>``

Everything is HTML-escaped **first**, then the (ASCII) markers are turned into
tags, so no author-supplied HTML can survive — this keeps the "never trust data
as HTML" rule while still letting the server emit formatted markup.
"""
import re

from django.utils.html import escape
from django.utils.safestring import mark_safe

# Matches **bold** on already-escaped text (the markers are plain ASCII, so
# escaping never touches them). Non-greedy, no newlines inside a span.
_BOLD = re.compile(r"\*\*(.+?)\*\*")


def _inline(escaped_text: str) -> str:
    """Apply inline **bold** to a run of already-escaped text."""
    return _BOLD.sub(r"<strong>\1</strong>", escaped_text)


def body_to_html(body: str) -> str:
    """Convert a patch-note body to safe HTML. Returns a mark_safe string."""
    if not body:
        return mark_safe("")

    out = []
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw_line in body.splitlines():
        line = raw_line.rstrip()

        if line.startswith("## "):
            close_list()
            out.append(f"<h3 class=\"pn-body__h\">{_inline(escape(line[3:]))}</h3>")
        elif line.startswith("- "):
            if not in_list:
                out.append("<ul class=\"pn-body__list\">")
                in_list = True
            out.append(f"<li>{_inline(escape(line[2:]))}</li>")
        elif line == "":
            close_list()
        else:
            close_list()
            out.append(f"<p>{_inline(escape(line))}</p>")

    close_list()
    return mark_safe("\n".join(out))
