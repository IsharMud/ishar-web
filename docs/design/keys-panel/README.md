# Keys & commands panel — verification proofs

Headless-Chromium screenshots of `#keys-pop`, rendered against the real
`hud.css` and the real key registry: the preview loads `hud.js` and calls
`IsharHUD.keyHelp()`, and the panel is built by the same `buildKeysPanel()`
source extracted from `connect.html`. Nothing here is hand-authored markup.
See `docs/design/decisions.md` (2026-07-28, "Keys & commands: one registry,
two surfaces, and a rule").

- `shot-full.png` — every group at once (the dialog's `max-height` lifted).
- `shot-desktop.png` — as shipped at 1280px: 640px dialog, scrolls internally.
- `shot-phone.png` — a true 390px viewport; rows stack, dialog scrolls in place.
- `shot-gear.png` — the gear menu's `.setting-link` row that opens it.
- `shot-hud-off.png` — a `hud: true` group while the interface is hidden.

Regenerate:

```
python3 build_preview.py                       # writes preview-keys*.html
python3 shot.py $PWD/preview-keys.html out.png 390 844 false
```

`shot.py` drives headless Chromium through Playwright rather than
`--screenshot`: Chromium clamps a headless window to 500px wide, so
`--window-size=390` yields a 500px layout cropped to 390 — phone-width proof
that silently isn't one.
