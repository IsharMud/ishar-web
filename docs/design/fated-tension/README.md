# Fated S16: Tension on the web — verification proofs

Headless-Chromium screenshots rendered through the real site against a
throwaway **sqlite** build of the game-owned tables (`build_db.py` creates
every `managed = False` table from the models, runs the ishar-mud migrations
that seed the knot menu and the Tension achievements, then inserts the
fixture from the spec: an account with woven 28 / loose 2 / best 4 /
lifetime 4, a Fated character locked at 4 with knots mask 65, Frostbite
bound at 50 and a severed thread). `render.py` hits every page with the
Django test client and checks the numbers the formulas predict;
`shots*.js` take the 390px and 1280px screenshots with Playwright and
report horizontal overflow and page errors. `verify_settings.py` and
`autologin.py` are the harness-only settings (sqlite, migrations off, a
`?as=<account>` login shim) — never production.

Decisions: `docs/design/decisions.md` (2026-10-15, three entries).

- `player_aelwyn_*.png` — the fixture character: Tension panel (4 · 3 of 10
  · banks 28), the two tied knots, the Loom with Frostbite (rare, 0.5) and
  the severed Bless.
- `player_lanya_desktop.png` — the loom is asking for knots (locked −1).
- `player_wren_phone.png` — at the summit, Tension 7, banks 38.
- `portal_tyrell_phone.png` / `portal_loom_phone.png` — the portal: the
  lifetime-best pill, the Achievements card, the Loom with the burden scale.
- `leaders_tension_*.png` / `leaders_lifetime_desktop.png` — accounts by best
  completed climb; Tyrell above Boric on woven essence at equal Tension.
- `achievements_tyrell_phone.png` / `achievements_anon_desktop.png` — the
  catalog, hidden trophy omitted, title and point rewards.
- `hud_tension_*.png` — the web client in demo mode: the `T4 · 3/10` pill
  and the Tension section of the Season overlay (desktop window, phone sheet).
- `fated_*.png` — the explainer. `knots_tyrell_*.png` — the knot menu with
  Aelwyn's tied knots marked. `season_phone.png` — the themed season page.

Not verified here: the live MariaDB and the game's real GMCP push.
