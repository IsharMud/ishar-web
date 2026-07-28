# Admin HUD — verification proofs

Headless-Chromium screenshots of the admin tier (isharmud/ishar-web#183 /
isharmud/ishar-mud#1888), rendered against the **real** `connect.html` markup,
`hud.js`, and `hud.css` with the `?demo=admin` staff fixtures. The harness
(`build_preview.py`) fakes only the Django template layer (static paths, `{%
bi %}`, auth booleans) — everything the shots show is the shipped client code.

```
python3 build_preview.py
chromium --headless=new --allow-file-access-from-files \
    --virtual-time-budget=5000 --window-size=1280,800 \
    --screenshot=shot-desktop.png 'file://…/preview.html?demo=admin'
# &open=<overlay key> clicks a launcher after load (dock button on phones)
```

- `shot-desktop.png` — the admin re-tier: attack cluster + XP strip gone,
  admin strip live (Eternal pill · `#41230 a rusty dagger` set-o chip ·
  `Ritani (30)`), staff launchers in the micro-menu.
- `shot-who.png` — Who overlay with the WhoExtra staff lines (rank pills,
  room #vnum, idle, cyan invis, red snoop edge, account names).
- `shot-zones.png` — Zones overlay: filter, live/unlive chips, regen meters,
  `try 3` failing pill, current-zone accent edge, noregen/skip flags.
- `shot-admin.png` — Admin overlay: game-state controls, season block with
  Forger controls hidden (`can_season: false` fixture), world clock/moons.
- `shot-inspect.png` — Inspector on a person Admin.Stat frame.
- `shot-phone*.png` — the same at a true 390px: admin strip fits, Who and
  Zones open in the bottom sheet.

**Known harness artifact:** at 390px the *document* measures 500px wide in
these shots because the headless DOM-renderer xterm never runs the fit addon
and the vitals bar sizes against it (`?demo=1` measures identically, with no
admin element in the offender list) — the real client fits the terminal and
passed the 6b mobile checklist. The admin surfaces add no overflow of their
own; zone rows wrap their flags/status under the name at phone width.

Delete this directory if the admin HUD is ever redesigned wholesale.
