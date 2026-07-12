# Ishar Web — Design System

This is the living source of truth for how ishar-web looks and why. It exists so
the site can be faceflifted **incrementally and coherently** — every page we
touch should pull from the same tokens, components, and principles instead of
inventing a new look.

Read this first, then:

- **[tokens.md](tokens.md)** — the palette: colors, surfaces, text, semantics,
  radii, motion. The variables everything keys off.
- **[components.md](components.md)** — the component catalog: what exists, its
  canonical markup, and where it's used.
- **[decisions.md](decisions.md)** — the running log of design decisions (ADR
  style). Append here whenever a call is made; don't relitigate settled ones.

If you're an agent or a human about to change any visual surface: skim the
principles below, grab the right tokens/components, and if you introduce or
change a convention, **record it in `decisions.md` and update the catalog.**

> **Green-field mandate.** We design ishar-web as if it were green field — **no
> concern with breakage or comms, just optimal, unhandcuffed design** (see
> `decisions.md`, and `../../CLAUDE.md`). Where a cleaner design exists, rebuild
> rather than patch. The roadmap below covers the whole site, public pages
> included, not only staff tooling.

---

## The one-paragraph summary

Ishar is **dark-only**, built on **Bootstrap 5.3.8** + **Bootstrap Icons 1.13.1**
(both self-hosted), with a **single amber accent** (`#fa7`) on light-grey text
(`#d6d6d7`). The whole site — public pages and staff tooling alike — speaks one
**layered-grey token + component language** (the `--ac-*` tokens and `.ac-*`
components, loaded globally), with amber reserved for brand, focus, and live
state. The old black+amber-outline "classic" layer is retired; only the web
client keeps an extra HUD-domain vocabulary on top of the shared tokens.

---

## Principles

1. **Dark-only, no toggle.** `<html data-bs-theme="dark">` is forced in
   `layout.html`. Design for dark; don't add a light theme.
2. **Amber is the accent, used sparingly.** `#fa7` marks brand, focus, primary
   actions, headers, and "live" state — not large fills. Overusing it flattens
   the hierarchy.
3. **Semantic colors are fixed.** ok = green, info = blue, warn = orange,
   danger = red, immortal = cyan. Same meaning everywhere (see tokens.md). Never
   repurpose them decoratively.
4. **Motion is subtle and optional.** Transitions/animations must always be
   wrapped by `@media (prefers-reduced-motion: reduce)`. No motion is load-bearing.
5. **Accessible by default.** Real focus styles (`:focus-visible`), `aria-*` on
   interactive/icon elements, sufficient contrast, and **JS updates the DOM with
   `textContent`, never `innerHTML`**, for anything derived from data.
6. **No new frontend libraries; self-host everything.** We ship Bootstrap +
   Bootstrap Icons and a little vanilla JS. Don't add a framework, a CDN
   dependency, or a web font without a decision entry.
7. **Mobile-first — a gating requirement, not a vibe.** The playerbase deploys
   and plays from phones. Every surface must pass the **mobile checklist** in
   `decisions.md` (no horizontal overflow, ≥16px form fields, coarse-pointer
   tap targets, no hover-only affordances or sticky lifts, stacked shell rows,
   compact chrome, 390px screenshot proof) before it ships.
8. **Icons via the SVG sprite.** Prefer
   `<svg class="bi"><use href="…bootstrap-icons.svg#name"></svg>` over the font
   classes — it inherits `currentColor` and scales cleanly.

---

## Visual layers (and where each applies)

The convergence is done: one language, one page-specific dialect.

| Layer | Where | Look | Source |
|---|---|---|---|
| **Console** (site-wide) | Every page — public content, portal, staff tooling, the shell | Layered greys + restrained amber, heroes, panels, rows, pills | `apps/core/static/css/style.css` (tokens + shell) + `apps/core/static/css/admin-console.css` (components, loaded globally) |
| **HUD** (dialect) | The web telnet client (`/connect`) | The console tokens plus HUD-domain colors (vitals, gold, edge, moons) and denser panels | `apps/connect/static/css/hud.css` |

**Stance:** there is no separate "classic" public look anymore (retired with
roadmap #7 — see decisions.md). Amber-border remnants survive only as brand
accents (navbar bottom edge, hero left edges, the navbar toggler). The HUD's
structural colors reference `--ac-*` directly; its `--hud-*` tokens cover only
HUD-domain meanings.

---

## Facelift roadmap

Incremental, page-by-page. Do the two enablers early so later pages are cheap.

### Enablers
- **E1 · Shared token base.** ✅ **done** — the `--ac-*` tokens live in the
  `:root` of `style.css` (loaded globally); `admin-console.css` is components
  only, and `hud.css` keeps only HUD-domain tokens on top of the shared set.
- **E2 · Shared components.** ✅ **started** — the `ishar` template tag library
  (`{% bi %}` icons, `{% crumb %}` breadcrumbs) + `partials/` exist; new/touched
  templates must use them. Old templates migrate as each page is facelifted.

### Page adoption order
Staff surfaces first (highest value, lowest risk — few users, we control them):

| # | Surface | Status |
|---|---|---|
| 1 | Deploy console (`/portal/deploy`) | ✅ done — the reference implementation |
| 2 | Feedback triage (`/feedback`) | ✅ done — tiles, chips, rows, timeline |
| 3 | Processes / other Django-admin-adjacent staff pages | ✖ closed — lives in Django admin, nothing to facelift (see decisions.md) |
| 4 | Portal (`/portal`) + global nav/layout shell | ✅ done — shell on console surfaces, portal rebuilt |
| 5 | Leaders, Challenges (DataTables pages) | ✅ done — `.ac-table` for leaders, challenge rows; jQuery/DataTables dropped from both |
| 6 | Connect HUD (align tokens) | ✅ done — structural colors are `--ac-*`; only vitals/flavor stay `--hud-*` |
| 6b | Connect HUD session UX (first-class mobile + premium desktop) | ✅ done — terminal-first phone dock/sheet, collapsible desktop columns, HUD on by default |
| 7 | Home, help, errors, public content | ✅ done — every remaining public template rebuilt on the console components; jQuery/DataTables deleted; classic CSS retired |

**The page-adoption roadmap is complete.** Future design work is incremental:
keep new surfaces on the tokens/components, extend the catalog deliberately
(decision entry + styleguide + catalog update), and treat any reappearance of
a retired pattern as a bug.

### Near-term addition
- **`/styleguide`** (Eternal+): ✅ built — renders every token and component
  live, linked from the Portal dropdown. The fastest way to build a consistent
  page and eyeball regressions.

---

## How to use this when changing a page

1. Reach for an existing **component** (components.md). If it's close, extend it;
   don't fork it.
2. Use **tokens** (tokens.md) for every color/space/radius — no ad-hoc hex.
3. Respect the **principles** above (dark, sparing amber, fixed semantics,
   reduced-motion, a11y, no new libs).
4. If you make a genuinely new decision (a new component, a token change, a
   deviation), **add a dated entry to decisions.md** and update the catalog.
