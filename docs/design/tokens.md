# Design Tokens

The canonical palette and scales. Every color, surface, and radius on a
faceflifted page should come from here — no ad-hoc hex.

**Enabler E1 is done:** the `--ac-*` set (plus `--ishar-color`) is defined once
in the `:root` block of `apps/core/static/css/style.css`, which every page loads
via `layout.html`. Any stylesheet may reference these tokens without redefining
them.

Sources of truth:
- `apps/core/static/css/style.css` — **the canonical `:root` token block**, plus
  the classic-site rules (some still literal; they migrate as pages are touched).
- `apps/core/static/css/admin-console.css` — the component layer built on the
  tokens (no token definitions of its own).
- `apps/connect/static/css/hud.css` — HUD-domain tokens only (vitals,
  resources, world flavor — see below); everything structural references the
  shared `--ac-*` set directly.

---

## Brand

| Token | Value | Meaning |
|---|---|---|
| `--ac-accent` / `--ishar-color` | `#fa7` | The Ishar amber. Brand, focus, primary/live accents. Use sparingly. |
| `--ac-accent-2` | `#ffd7b0` | Lighter amber for text/marks on amber washes (contrast). |

The full hex of the brand amber is `#ffaa77` (that's what the `theme-color` /
tile meta use); `#fa7` is the shorthand used in CSS.

---

## Surfaces (dark, layered)

Surfaces step **up in lightness** as they come forward. Classic panels are pure
black with an amber outline; Admin Console panels use the layered greys.

| Token | Value | Use |
|---|---|---|
| `--ac-bg` | `#0c0c0d` | Deepest surface — page/console background, inset wells. |
| `--ac-panel` | `#131316` | Panel / card surface. |
| `--ac-elev` | `#1c1c22` | Raised / hover surface, chips, icon tiles. |
| `--ac-border` | `#2a2a30` | Default hairline border. |
| `--ac-border-2` | `#3a3a44` | Stronger border (hover/active/inputs). |

The classic pure-black panel surfaces (`.card`/`.list-group` on `#000`, the
`#323639` element backgrounds) were retired with roadmap #7 — public pages now
sit on the same layered greys.

The HUD uses these `--ac-*` surfaces directly (the old duplicate `--hud-bg` /
`--hud-panel` / `--hud-border` aliases are gone). The web terminal itself stays
true black (`#000`) to match the xterm theme background — that's game canvas,
not a surface token.

---

## Text

| Token | Value | Use |
|---|---|---|
| `--ac-text` | `#d6d6d7` | Body text. The canonical foreground everywhere. |
| `--ac-dim` | `#8a8a92` | Muted text: labels, hints, secondary meta. |
| — | `#c7c7c9` | Console/log body text (slightly dimmer than body). |

Headings, `<label>`, `<strong>`, `<th>`, and `.text-ishar` render in **amber**
(`--ishar-color`) — the site's "highlighted text" convention. Bare (classless)
form elements default to console-field styling (`--ac-bg` / `--ac-border-2` /
`--ac-text`) so Django-rendered forms look native without markup changes.

---

## Links (classic site)

| State | Value |
|---|---|
| link | `#09f` (bright blue) |
| active / visited | `#6082b6` (muted blue) |
| hover | `#d6d6d7` (body text) |

Admin Console surfaces generally avoid raw links in favor of buttons/pills; when
a link is needed there, prefer `--ac-accent` on hover.

---

## Semantic colors (fixed meanings)

Do not repurpose these. They mean the same thing on every surface.

| Token | Value | Meaning |
|---|---|---|
| `--ac-ok` | `#4cbb17` | Success, healthy, safe, "moves" (HUD). Also `.message-success`, active season. |
| `--ac-info` | `#4a86cf` | Informational, in-progress, "mana" (HUD). |
| `--ac-warn` | `#f80` | Caution / heads-up. Also `.message-warn`/`.message-warning`. |
| `--ac-danger` | `#d64b4b` | Destructive / error (Admin Console). Also "health" (HUD). |
| — (classic danger) | `#d02b2b` | `.message-error`, dead/survival/hardcore players. |
| `--ac-immortal` | `#00b7eb` | Immortal accounts (god/forger/eternal/artisan/immortal/consort). Cyan. Pill variant: `.ac-pill--immortal`. |

**HUD-domain tokens** (`hud.css` `:root` — meanings that exist only in the web
client). The vitals triple aliases the shared semantics: `--hud-hp:
var(--ac-danger)`, `--hud-mp: var(--ac-info)`, `--hud-mv: var(--ac-ok)`. The
rest have no site-wide equivalent:

| Token | Value | Meaning |
|---|---|---|
| `--hud-gold` | `#cdcd00` | Currency, shop, pinned/favourite marks (plus `--hud-gold-wash` `rgba(205,205,0,.1)`). |
| `--hud-xp` | `#9a86e0` | XP hairline strip — a violet used nowhere else, so it reads unambiguously as XP without competing with the amber accent, green vitals, or terminal text. |
| `--hud-tgt` | `#a0408a` | Opponent health bar. |
| `--hud-mm` | `#a05ad0` | Metamagic bar. |
| `--hud-edge` | `#d08a3a` | Edge resource bar. |
| `--hud-event` | `#e8b04b` | World event flags. |
| `--hud-moon` | `#9aa6c8` | Moon phases. |
| `--hud-ter-*` | see below | Map terrain fills (canvas reads them via `getComputedStyle`). |

**Map terrain fills** (`--hud-ter-*`): muted, desaturated room fills for the
HUD map — the map is background; amber (current room / path) is the only thing
that pops. `indoor #26262c` · `city #33333b` · `field #2b3a28` ·
`forest #243626` · `hill #38332a` · `mountain #3c3c40` · `water #24384d`
(shallow) · `deep #1d2e42` · `under #1a2a3c` (underwater) · `desert #40382a` ·
`beach #3d3a2e` · `swamp #2c3626`. Forest Path / Mountain Path reuse
`field` / `hill`. Map state inks come from the shared tokens: current room
ring `--ac-accent`, note dots `--ac-info`, locked doors `--ac-warn`, death
corners `--ac-danger`, edges/stubs `--ac-border-2` / `--ac-dim`.

**Player-status vocabulary** (from `style.css`, used by `player_css`):
- Immortals (`.god-player` … `.consort-player`): `var(--ac-immortal)`, with
  emoji affix (`😇` god, `👼` other immortals).
- Dead / survival / hardcore (`.dead-player`, …): `#d02b2b`; visited `#fa8072`;
  hover `#f00`; affix `☠️`.

**Status → color maps** (data-driven) live on the models, e.g. feedback's
`status_css` (`apps/feedback/models/feedback.py`) emits Bootstrap contextual
names (`success`/`danger`/`info`/`primary`/`warning`/`secondary`). Keep those in
the model, render with Bootstrap `text-bg-*` or an `.ac-pill--*` modifier.

---

## Translucent washes

Subtle tints for selected/active states and hero banners.

| Token | Value |
|---|---|
| `--ac-wash` | `rgba(255,170,119,.12)` (amber) |
| `--ac-ok-wash` | `rgba(76,187,23,.12)` |
| `--ac-info-wash` | `rgba(74,134,207,.14)` |
| `--ac-warn-wash` | `rgba(255,136,0,.12)` |
| `--ac-danger-wash` | `rgba(214,75,75,.14)` |

---

## Radii & motion

| Token | Value | Use |
|---|---|---|
| `--ac-radius` | `.6rem` | Panels, hero, console. |
| `--ac-radius-sm` | `.4rem` | Inputs, toggles, buttons, chips. |
| pill radius | `999px` | Status pills, segmented control. |

Motion: transitions are ~`.15s`; the few keyframes (`ac-pulse`, `ac-rotate`,
`ac-glow`) live in `admin-console.css`. **All motion is disabled under**
`@media (prefers-reduced-motion: reduce)` — match that whenever you add any.

---

## Typography

- **No custom web fonts.** Body uses the Bootstrap system stack.
- **Monospace** (`var(--bs-font-monospace, monospace)`) for logs, terminals,
  service names, and code — anywhere "machine" text belongs.
- **Section labels** are the dashboard signature: `UPPERCASE`, `font-weight:700`,
  `letter-spacing:~.09em`, in `--ac-dim` (see `.ac-panel__h`). Use them for panel
  headers on admin surfaces.
- Numeric readouts that tick (timers, counts) use
  `font-variant-numeric: tabular-nums` so they don't jitter.
