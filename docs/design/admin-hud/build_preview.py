"""Render the real /connect client as a static page for headless screenshots.

The live page needs Django + the game; this harness fakes only the template
layer — the markup, hud.js/hud.css, and the demo feeds are the real files.
`?demo=admin` drives the staff fixtures; `&open=<overlay>` clicks a launcher
after load so overlay shots need no interaction.

    python3 build_preview.py            # writes preview.html
    chromium --headless=new --allow-file-access-from-files \
        --virtual-time-budget=4000 --window-size=1280,800 \
        --screenshot=shot.png 'file://.../preview.html?demo=admin&open=zones'
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
content = re.sub(r'\{\{ user\.is_authenticated\|yesno:"true,false" \}\}', "false", content)
content = re.sub(r"\{\{ WEBSITE_TITLE \}\}", "Ishar MUD", content)
content = re.sub(r"\{%\s*url\s+[^%]+%\}", "#", content)
content = re.sub(r"\{\{[^}]*\}\}", "", content)
content = re.sub(r"\{%[^%]*%\}", "", content)

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
<title>connect preview</title>
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
<script>
window.addEventListener("load", function () {{
    setTimeout(function () {{
        var open = new URLSearchParams(location.search).get("open");
        if (open) {{
            // Phones open panels via the dock; desktop via the micro-menu.
            var sel = window.matchMedia("(max-width: 767.98px)").matches
                ? '[data-panel="' + open + '"]'
                : '[data-overlay="' + open + '"]';
            var b = document.querySelector(sel);
            if (b) b.click();
        }}
        document.title = "READY";
    }}, 400);
}});
</script>
</body></html>"""

(HERE / "preview.html").write_text(out)
print("wrote", HERE / "preview.html")
