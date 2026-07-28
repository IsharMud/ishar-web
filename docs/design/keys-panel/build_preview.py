import re, pathlib
R = pathlib.Path(__file__).resolve().parents[3]
html = (R/'apps/connect/templates/connect.html').read_text()

def slice_between(text, start, end):
    i = text.index(start); j = text.index(end, i) + len(end)
    return text[i:j]

registry = slice_between(html, "var KEYS_TERMINAL = [", "return KEYS_TERMINAL.concat(hud, KEYS_CLIENT);\n    }")
render = slice_between(html, "    function keyNote(text, cls) {", "            keysBody.appendChild(sec);\n        });\n    }")

tokens = (R/'apps/core/static/css/style.css').read_text()
tokens = tokens[tokens.index(':root {'):tokens.index('.border-ishar')]
hudcss = (R/'apps/connect/static/css/hud.css').read_text()

panel = slice_between(html, '<div id="keys-pop"', '<div id="keys-body"></div>\n    </div>')
panel = re.sub(r'\{%\s*bi "x-lg"\s*%\}',
               '<svg class="bi" width="14" height="14" viewBox="0 0 16 16">'
               '<path d="M2 2l12 12M14 2L2 14" stroke="currentColor" stroke-width="2" fill="none"/></svg>', panel)
panel = panel.replace(' hidden>', '>', 1)


def build(name, app_class="", extra_css=""):
    out = f"""<!doctype html><html data-bs-theme="dark"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{tokens}
body {{ margin:0; background:#000; color:var(--ac-text); font-family: system-ui, sans-serif; min-height:100vh; }}
{hudcss}
{extra_css}
</style></head><body>
{panel}
<script src="file://{R}/apps/connect/static/js/hud.js"></script>
<script>
(function() {{
    var app = document.createElement("div");
    app.className = "{app_class}";
    var keysBody = document.getElementById("keys-body");
{registry}
{render}
    buildKeysPanel();
    if (!(window.IsharHUD && window.IsharHUD.keyHelp)) document.title = "HUD MISSING";
}})();
</script>
</body></html>"""
    pathlib.Path(name).write_text(out)
    print("wrote", name)


FULL = "#keys-pop { position: static; transform: none; max-height: none; margin: 16px auto; }"
build("preview-keys.html")
build("preview-keys-full.html", extra_css=FULL)
build("preview-keys-off.html", app_class="hud-off", extra_css=FULL)
