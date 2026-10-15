"""Render every touched page with the Django test client against the sqlite
fixture, save the HTML, and check the numbers the formulas predict."""
import html as htmlmod, os, re, sys
sys.path.insert(0, "/home/user/ishar-web"); sys.path.insert(0, os.path.dirname(__file__))
os.environ["DJANGO_SETTINGS_MODULE"] = "verify_settings"
import django; django.setup()
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import update_last_login
from django.test import Client
from apps.accounts.models import Account

user_logged_in.disconnect(update_last_login, dispatch_uid="update_last_login")
OUT = os.path.join(os.path.dirname(__file__), "out"); os.makedirs(OUT, exist_ok=True)

def text(html):
    html = re.sub(r"<script.*?</script>", "", html, flags=re.S)
    return htmlmod.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)))

failures = []
def check(name, html, *needles, absent=()):
    t = text(html)
    for n in needles:
        if n not in t:
            failures.append(f"{name}: missing {n!r}")
    for n in absent:
        if n in t:
            failures.append(f"{name}: unexpected {n!r}")

def get(client, path, name, status=200):
    r = client.get(path, HTTP_HOST="testserver")
    if r.status_code != status:
        failures.append(f"{name}: HTTP {r.status_code} for {path}")
    html = r.content.decode() if r.status_code == 200 else ""
    open(os.path.join(OUT, name + ".html"), "w").write(html)
    return html, r

tyrell = Account.objects.get(account_name="Tyrell")
boric = Account.objects.get(account_name="Boric")
selra = Account.objects.get(account_name="Selra")
staff = Account.objects.get(account_name="Eternal")

c = Client(); c.force_login(tyrell)
html, _ = get(c, "/player/Aelwyn/", "player_aelwyn")
check("player_aelwyn", html,
      "tension 4",                       # hero pill: locked value is authoritative
      "4 Tension", "3 of 10 Remorts",
      "28 Banks on ascension",           # bank(4) = 16 * 180 / 100 = 28
      "Locked at 4 when this thread was spun — knots 3.5, loom burden now 0.5",          # Weave Watches 2.0 + Exposed 1.5; Frostbite rare 0.5
      "The Weave Watches", "Exposed", "2.0", "1.5",
      "28 Woven", "2 Loose", "4 Best this season", "4 Lifetime best",
      "Frostbite", "rare", "level 50", "0.5",
      "Bless", "severed", "burden 0.5",
      "Help: Tension · Knots · Ascension · Woven")
html, _ = get(c, "/player/Rook/", "player_rook")
check("player_rook", html, absent=("Tension", "The Loom"))
html, _ = get(c, "/portal/", "portal_tyrell")
check("portal_tyrell", html, "tension 4", "28 Woven", "2 Loose", "Bound Threads (1)", "Frostbite", "severed", "Achievements", "10 pts")

html, _ = get(c, "/leaders/", "leaders")
check("leaders", html, "Characters", "Tension", "Lifetime Tension")
html, _ = get(c, "/leaders/tension/", "leaders_tension")
t = text(html[html.index("<tbody>"):html.index("</tbody>")]) if "<tbody>" in html else ""
order = [m for m in re.findall(r"\b(Tyrell|Boric|Selra|Nobody)\b", t)]
# season: Tyrell (4, woven 28) > Boric (4, woven 16) > Selra (3); Nobody (0) absent
if order[:3] != ["Tyrell", "Boric", "Selra"] or "Nobody" in order:
    failures.append(f"leaders_tension: order {order}")
check("leaders_tension", html, "Only a completed climb counts", "Aelwyn", "3 accounts")
html, _ = get(c, "/leaders/tension/lifetime/", "leaders_lifetime")
t = text(html[html.index("<tbody>"):html.index("</tbody>")]) if "<tbody>" in html else ""
order = [m for m in re.findall(r"\b(Tyrell|Boric|Selra|Nobody)\b", t)]
if order[:3] != ["Selra", "Boric", "Tyrell"]:
    failures.append(f"leaders_lifetime: order {order}")

html, _ = get(c, "/achievements/", "achievements_tyrell")
check("achievements_tyrell", html, "The First Tightening", "Pulled Taut", "Wound Tight", "title: the Rewoven",
      "earned", "10 pts", "25 pts", "General · Tension", "Challenge Novice", "100 essence",
      absent=("The Loom's Equal", "Loom&#x27;s Equal"))
anon = Client()
html, _ = get(anon, "/achievements/", "achievements_anon")
check("achievements_anon", html, "The First Tightening", "Log in", absent=("The Loom's Equal",))
cs = Client(); cs.force_login(selra)
html, _ = get(cs, "/achievements/", "achievements_selra")
check("achievements_selra", html, "The Loom's Equal", "title: the Loom's Equal", "hidden")

# Boric: an untied life (Lanya) and a between-lives thread (Tam); passive burden per tier.
cb = Client(); cb.force_login(boric)
html, _ = get(cb, "/player/Lanya/", "player_lanya")
check("player_lanya", html, "The loom is asking for knots", "Divine Purpose", "tier 3", "0.6", "Inferno", "legendary", "1.5", "burden 2.1",
      absent=("tension 0",))
html, _ = get(cb, "/player/Tam/", "player_tam")
check("player_tam", html, "between lives")
# Selra is private: Tyrell may not see Wren; staff may, and sees the summit line.
_, r = get(c, "/player/Wren/", "player_wren_denied", status=404)
cst = Client(); cst.force_login(staff)
html, _ = get(cst, "/player/Wren/", "player_wren_staff")
check("player_wren_staff", html, "stands at the summit — the eleventh prayer ascends", "7 Tension", "10 of 10", "38 Banks on ascension")   # bank(7) = 16 * 240 / 100

# Help mirror: the game's helptab served through the site's parser.
for topic in ("Tension", "Knots", "Ascension", "Woven"):
    html, _ = get(anon, f"/help/{topic}/", f"help_{topic.lower()}")
    check(f"help_{topic}", html, topic)
check("help_Tension", open(os.path.join(OUT, "help_tension.html")).read(), "Tension is the measure of how tightly the weave is drawn against you")
check("help_Ascension", open(os.path.join(OUT, "help_ascension.html")).read(), "the eleventh prayer ascends")
check("help_Woven", open(os.path.join(OUT, "help_woven.html")).read(), "Loose essence is not lost on death")
_, r = get(anon, "/help/Loose/", "help_loose", status=302)
if r.status_code == 302 and "/help/Woven/" not in r["Location"]:
    failures.append(f"help_loose: redirected to {r['Location']}")
_, r = get(anon, "/help/Burden/", "help_burden", status=302)


# --- follow-up: explainer, knot menu, theming --------------------------
html, _ = get(anon, "/fated/", "fated_anon")
check("fated_anon", html, "The Fated", "One thread", "The draw", "The bind", "Knots", "Burden and Tension",
      "common 0.2", "legendary 1.5", "16 woven essence at Tension 0", "The summit", "Woven and loose",
      "Loose essence is not lost on death", "the Rewoven", "help tension", "this season",
      absent=("Loom's Equal", "heat", "meta-progression", "roguelite", "build"))
html, _ = get(anon, "/fated/knots/", "knots_anon")
check("knots_anon", html, "16 knots", "24.0 at the top", "The Weave Watches", "Stanched", "Unmended", "tighter",
      "Loosed Knots", "4.5", "Skill levels are capped at 80.")
if "ac-row--tied" in html:
    failures.append("knots_anon: a knot marked tied for an anonymous viewer")
html, _ = get(c, "/fated/knots/", "knots_tyrell")
check("knots_tyrell", html, "Aelwyn's tied knots are marked below", "locked at Tension 4")
t = text(html)
if t.count(" tied") < 2:
    failures.append("knots_tyrell: expected two tied knots marked")
html, _ = get(cb, "/fated/knots/", "knots_boric")
check("knots_boric", html, "The loom is asking Lanya for knots")
html, _ = get(anon, "/season/", "season")
check("season", html, "Fractured Threads", "How a Fated life runs", "the knot menu")
check("footer", html, "Fractured Threads")
html, _ = get(anon, "/help/", "help_index")
check("help_nav", html, "The Fated")
html, _ = get(c, "/portal/", "portal_burden")
check("portal_burden", html, "Every bound thread weighs by rarity", "rare 0.5")
print("\n".join(failures) if failures else "ALL CHECKS PASSED")
