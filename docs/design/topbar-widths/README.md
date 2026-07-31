# Topbar at every width — verification proofs

Headless-Chromium screenshots of `#hud-topbar` rendered through the real
client: `build_preview.py` fakes only the Django template layer, so the
markup, `hud.css`, `hud.js` and the `?demo=1` feeds are the shipped files and
the bar is built by the real `renderVitals()` / `renderSessionTabs()`.
See `docs/design/decisions.md` (2026-07-31, "The topbar tells the same story
at every width").

`before-*.png` are the same harness run against the parent commit.

- `before-1400.png` / `after-1400.png` — wide desktop. After: the character
  is a real `.sess-tab` chip beside the `+`, the duplicate `#connection-status`
  dot is gone (`.conn-ok`), and the bar is a row shorter.
- `before-700.png` / `after-700.png` — a snapped or zoomed desktop window,
  below the 768px breakpoint. **This is the reported bug**: before, the whole
  world strip (hour, season, events, moons) is absent; after, it reflows.
- `before-390.png` / `after-390.png` — a true 390px phone.
- `after-1400-multi.png` / `after-390-multi.png` — three and two sessions;
  close controls return and the `+` hides at `MAX_SESSIONS`.

Regenerate:

```
python3 build_preview.py
node shot.mjs $PWD/preview.html after-390.png 390 Aelwyn
node shot.mjs $PWD/preview.html after-1400-multi.png 1400 Aelwyn,Thalindra,Boric
```

Two harness artifacts, neither in the real client: icon buttons render as
empty rounded boxes because the Bootstrap SVG sprite can't be fetched
cross-document over `file://`, and the action-bar/affect tiles below the bar
belong to the HUD, not the topbar. `Aelwyn` is the seeded roster name because
it is also the `Char.Status` name in the demo fixture — in play both come
from the same GMCP packet.
