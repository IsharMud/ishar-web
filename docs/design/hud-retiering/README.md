# HUD re-tiering — proposal mock

Throwaway design mock backing the HUD re-tiering proposal issue. Not the live
client: glyphs are stand-ins (not the real game-icons sprite) and data is the
`/connect?demo=1` sample feeds, so these prove **layout and hierarchy**, not
runtime behavior.

Regenerate the HTML + screenshots:

```
python3 build_preview.py
# then render each preview-*.html with headless Chromium (see the repo's
# verification notes in CLAUDE.md)
```

Delete this directory once the re-tiering lands.
