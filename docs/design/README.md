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
(`#d6d6d7`). The public site's identity is **black panels outlined in amber**
(`.border-ishar`). Newer, richer surfaces (the connect HUD, the deploy console)
use a **layered-grey token system** that reads more like a premium dashboard.
The direction is to unify these behind one shared token + component layer while
keeping the amber brand.

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
7. **Mobile-first.** The playerbase deploys and plays from phones. Every admin
   tool and page must be usable at a phone width.
8. **Icons via the SVG sprite.** Prefer
   `<svg class="bi"><use href="…bootstrap-icons.svg#name"></svg>` over the font
   classes — it inherits `currentColor` and scales cleanly.

---

## Visual layers (and where each applies)

Three visual layers coexist today. This is deliberate, but they should share
tokens and converge over time.

| Layer | Where | Look | Source |
|---|---|---|---|
| **Classic** | Public site (home, portal, leaders, help, …) | Black panels, amber `.border-ishar` outline, blue links | `apps/core/static/css/style.css` |
| **HUD** | The web telnet client (`/connect`) | Layered greys, colored vitals bars, gradient banner | `apps/connect/static/css/hud.css` |
| **Admin Console** | Staff tooling (deploy console; feedback next) | Layered greys + amber accents, terminal panels, status pills | `apps/core/static/css/admin-console.css` |

**Stance:** **staff/admin tooling uses the Admin Console language** (it should
feel like a purpose-built console). The **public shell keeps its amber-border
look for now** — but under the green-field mandate that's a starting point, not a
protected identity: public pages are in scope for the same convergence, and the
amber-border treatment stays only where it's genuinely the best design. All
layers draw from **one shared token + semantic vocabulary** (tokens.md). The HUD
predates the Admin Console layer but uses the same idea; over time its `--hud-*`
tokens should be expressed in terms of the shared set.

---

## Facelift roadmap

Incremental, page-by-page. Do the two enablers early so later pages are cheap.

### Enablers (do these first)
- **E1 · Shared token base.** Promote the Admin Console tokens (`--ac-*`) into a
  small base stylesheet that any page can include (or fold into `style.css`), so
  colors/surfaces/motion are defined once. Express `--hud-*` in terms of it.
- **E2 · Shared components.** ishar-web has **no template partials or template
  tags today** — markup is copy-pasted. Introduce `{% include %}` partials and a
  `templatetags` module for the repeating pieces (icon, status pill, stat tile,
  panel header, breadcrumb, empty state) so a component is defined once and
  restyled once.

### Page adoption order
Staff surfaces first (highest value, lowest risk — few users, we control them):

| # | Surface | Status |
|---|---|---|
| 1 | Deploy console (`/portal/deploy`) | ✅ done — the reference implementation |
| 2 | Feedback triage (`/feedback`) | next |
| 3 | Processes / other Django-admin-adjacent staff pages | later |
| 4 | Portal (`/portal`) + global nav/layout shell | later |
| 5 | Leaders, Challenges (DataTables pages) | later |
| 6 | Connect HUD (align tokens) | later |
| 7 | Home, help, errors, public content | last |

### Recommended near-term addition
- **A live `/styleguide` page** (staff-only) that renders every token and
  component from this doc, with copy-paste markup. It becomes the fastest way to
  build a consistent page and to eyeball regressions. Not built yet — a good
  next step once E1/E2 land.

---

## How to use this when changing a page

1. Reach for an existing **component** (components.md). If it's close, extend it;
   don't fork it.
2. Use **tokens** (tokens.md) for every color/space/radius — no ad-hoc hex.
3. Respect the **principles** above (dark, sparing amber, fixed semantics,
   reduced-motion, a11y, no new libs).
4. If you make a genuinely new decision (a new component, a token change, a
   deviation), **add a dated entry to decisions.md** and update the catalog.
