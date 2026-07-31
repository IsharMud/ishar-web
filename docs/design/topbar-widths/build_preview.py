"""Render the real /connect topbar as a static page for headless screenshots.

The live page needs Django + the game; this harness fakes only the template
layer — the markup, hud.js/hud.css and the demo feeds are the real files, and
the topbar is built by the real `renderVitals()` / `renderSessionTabs()`.

`?demo=1` supplies the HUD feeds but normally skips the socket, which would
pin every session at "connecting" and never let a `Char.Status` name reach a
tab. Two narrow overrides (below) let demo mode take the ordinary connect
path instead, against the stub WebSocket `shot.mjs` installs. Nothing in the
render path is touched.

    python3 build_preview.py                       # writes preview.html
    node shot.mjs $PWD/preview.html out.png 390    # a true 390px viewport
"""
import re
import pathlib

R = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
html = (R / "apps/connect/templates/connect.html").read_text()

STATIC_ROOTS = [R / "apps/connect/static", R / "apps/core/static"]


def static_url(path):
    for root in STATIC_ROOTS:
        if (root / path).exists():
            return "file://" + str(root / path)
    return path


content = html[html.index("{% block content %}") + len("{% block content %}"):]
content = content[:content.index("{% endblock content %}")]

content = re.sub(r"\{#.*?#\}", "", content, flags=re.S)
content = re.sub(
    r"""\{%\s*bi\s+"([\w-]+)"\s*%\}""",
    lambda m: (
        '<svg class="bi" width="16" height="16" fill="currentColor">'
        f'<use href="{static_url("bootstrap-icons/bootstrap-icons.svg")}#{m.group(1)}"/></svg>'
    ),
    content,
)
content = re.sub(
    r"\{%\s*static\s+'([^']+)'\s*%\}", lambda m: static_url(m.group(1)), content
)
content = content.replace("{% csrf_token %}", '<input type="hidden" name="csrfmiddlewaretoken" value="preview">')
content = content.replace(
    '{{ skill_icons|json_script:"ishar-skill-icons" }}',
    '<script id="ishar-skill-icons" type="application/json">{}</script>',
)
# Authenticated: the roster is account-gated and the multiplay "+" only
# renders for a logged-in account.
content = re.sub(r'\{\{ user\.is_authenticated\|yesno:"true,false" \}\}', "true", content)
content = re.sub(r"\{\{ WEBSITE_TITLE \}\}", "Ishar MUD", content)
content = re.sub(r"\{%\s*url\s+[^%]+%\}", "#", content)
content = re.sub(r"\{\{[^}]*\}\}", "", content)
content = re.sub(r"\{%[^%]*%\}", "", content)

# Let demo mode connect (to shot.mjs's stub socket) and rebuild a seeded
# roster, so sessions reach "connected" and tabs carry real character names.
OVERRIDES = [
    ("if (!isDemo) sess.connect();", "sess.connect();"),
    ("if (isDemo || !isAuthed) return null;", "if (!isAuthed) return null;"),
]
for old, new in OVERRIDES:
    assert old in content, f"harness override no longer matches: {old}"
    content = content.replace(old, new)

head_links = "\n".join(
    f'<link rel="stylesheet" href="{static_url(p)}">'
    for p in ("css/style.css", "css/admin-console.css", "css/xterm.min.css", "css/hud.css")
)
head_scripts = "\n".join(
    f'<script src="{static_url(p)}"></script>'
    for p in (
        "js/xterm.min.js", "js/addon-fit.min.js", "js/addon-web-links.min.js",
        "js/addon-serialize.min.js", "js/addon-search.min.js",
        "js/hud.js", "js/hud-map.js",
    )
)

out = f"""<!doctype html><html data-bs-theme="dark"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>connect topbar preview</title>
{head_links}
<style>
body {{ margin: 0; background: #000; }}
/* Headless xterm never runs the fit addon, so its default 80 cols would
   force the page wider than the phone viewport — an artifact the real
   client doesn't have. Cap it so the shots measure the actual layout. */
#terminal-container, .term-host, .xterm {{ max-width: 100vw; overflow: hidden; }}
</style>
{head_scripts}
</head><body class="connect-page">
{content}
</body></html>"""

(HERE / "preview.html").write_text(out)
print("wrote", HERE / "preview.html")
