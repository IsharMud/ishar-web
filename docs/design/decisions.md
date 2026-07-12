# Design Decisions Log

An append-only record of design decisions, newest first. Lightweight ADR: what
we decided, and why. When you make a real design call — a new component, a token
change, a deliberate deviation — add an entry. Don't relitigate settled ones;
supersede with a new dated entry if something genuinely changes.

Format: `## YYYY-MM-DD — Title` · **Decision** · **Why** · (optional) **Notes**.

---

## 2026-07-12 — The global shell moves to the console surfaces

**Decision.** The frame every page sits in — body, navbar, breadcrumb,
messages, `#content`, footer — now uses the layered-grey token surfaces:
`body` on `--ac-bg`, panels via the new `.shell-panel` (panel bg, hairline
border, `--ac-radius`), dropdown menus via `.shell-menu` (elev bg). Amber is
restrained to brand: nav text/icons, a 2px amber bottom edge on the navbar,
headings. Breadcrumbs become a quiet page-title line (no box; h2-sized crumbs
downsized by CSS so untouched templates inherit the fix). The logo slims to
8rem (5.5rem on phones). The heavy black + `.border-ishar` outline boxes are no
longer part of the shell — they live on only inside untouched page content, and
`.border-ishar` remains defined for them.

**Why.** The shell is the highest-leverage surface (every page, every visit).
Nesting the console pages inside a black+amber frame produced two competing
visual systems on one screen; one quiet frame lets both console surfaces and
classic content read well while pages migrate. Icons also converge on amber
(nav/breadcrumb) and dim (footer), replacing the blue/amber mishmash.

## 2026-07-12 — Portal adopts the console language; popovers retired there

**Decision.** `/portal` is rebuilt: hero (account, created, counts, essence +
privacy pills), gated tool grids using the new `.ac-link` navigation card,
characters as `.ac-rows` (immortals get an info pill and recede to a phrase;
mortals show class/race/alignment and nonzero lifetime stats as icon+number
meta), essence as `.ac-tile`s, upgrades as `.ac-kv`, and the private-profile
toggle as an `.ac-switch` whose result renders in an `.ac-note` via
`textContent` (the old `innerHTML` write is gone). Bootstrap tooltip/popover
help-icons are replaced by `.ac-panel__hint` prose with links — fewer JS
behaviors, better on phones.

**Why.** The portal is the account hub and the template other pages copy; it
was the largest remaining pile of pasted list-group/details markup.

## 2026-07-12 — Live style guide at /styleguide (Eternal+)

**Decision.** A staff-only page (`apps/core/views/styleguide.py`, linked from
the Portal dropdown and portal grid) renders every token and component live.
Page-specific demo CSS stays in the template's `<style>` block, not the shared
layer.

**Why.** The component set is now large enough that a copy-paste reference and
one-glance regression check pays for itself.

## 2026-07-12 — Roadmap #3 (Processes) is closed as not-a-surface

**Decision.** The "Processes" staff pages live in Django admin (jazzmin), not
in this site's template layer, and the admin's own notes mark its actions as
container-model relics (the Deploy Console replaced the actionable part).
There is nothing to facelift; removing the app entirely is tracked as game-repo
follow-up cleanup, not design work.

**Why.** Honest roadmap: a facelift line item that would restyle a dead surface
is entropy, not progress.

## 2026-07-11 — E1: shared tokens live in style.css

**Decision.** The `--ac-*` design tokens (plus `--ishar-color`) are defined once
in the `:root` block of `apps/core/static/css/style.css`, which every page loads
via `layout.html`. `admin-console.css` (and any future per-page stylesheet) is a
pure component layer that references those tokens without redefining them.
`--ac-warn-wash` was added to complete the wash set.

**Why.** One definition site means a palette change is a one-line edit, and any
page — public or staff — can adopt console components without a token import
dance. A separate `tokens.css` would add an HTTP request for a ~40-line block
that the global stylesheet can carry for free.

## 2026-07-11 — E2: shared markup via the `ishar` template tag library

**Decision.** Repeating markup is consolidated in
`apps/core/templatetags/ishar.py` (`{% load ishar %}`) plus partials under
`apps/core/templates/partials/`. First tags: `{% bi name css label %}` for
sprite icons (decorative by default, `role="img"` when labeled; output built
with `format_html` so labels are escaped) and `{% crumb label icon urlname
anchor active %}` for breadcrumb items. New/touched templates must use these
instead of pasting SVG/breadcrumb boilerplate; mass adoption across old
templates happens as each page is facelifted.

**Why.** The site had no partials or template tags — every icon and crumb was
copy-pasted. A tag is one place to fix accessibility, escaping, and markup.

## 2026-07-11 — Admin list views are row stacks, not data tables

**Decision.** Staff-tooling list surfaces use the `.ac-rows` / `.ac-row`
component — a bordered stack of wrapping flex rows (icon tile, main
title+meta, right-aligned status/actions) — rather than `<table>` markup.
Tables remain appropriate for genuinely tabular, column-comparable data
(leaders, challenges).

**Why.** Mobile-first is non-negotiable: tables force horizontal scrolling at
phone widths, while flex rows wrap gracefully. A triage list is a list of
records with actions, not a matrix — rows are the honest structure.

## 2026-07-11 — Status pills replace Bootstrap contextual badges on admin surfaces

**Decision.** Admin/staff surfaces render status as `.ac-pill` with semantic
modifiers, driven by a `status_pill` property on the model (e.g.
`Feedback.status_pill` → `ok/info/warn/danger/accent/muted`), returned alongside
`status_css` in action JSON so JS swaps `textContent` + `className`. Bootstrap
`text-bg-*` badges remain only on untouched classic pages until each is
facelifted.

**Why.** One status vocabulary on console surfaces; the color map stays on the
model (data-driven), the pill styling stays in the component layer.

## 2026-07-11 — Feedback triage adopts the Admin Console language

**Decision.** `/feedback` (dashboard + detail) is rebuilt as surface #2 of the
facelift: `ac-hero` with a live unacked pill, `ac-tile` KPI tiles that double as
filters (`--active` marks the applied one, zero counts render `--muted`),
`ac-chip` filter bar, `.ac-rows` report list, `ac-timeline` for comments
(system entries recede: dashed, dim, italic), `ac-kv` details, `ac-btn` action
panel, and `ac-quote` — monospace-on-deepest-surface — for verbatim report
bodies (they're captured game text; the terminal feel is deliberate).

**Why.** Highest-traffic staff surface after deploy; it exercised and hardened
the component set (tiles, chips, rows, timeline) the rest of the site will use.

## 2026-07-11 — Treat ishar-web as green field

**Decision.** Design and refactor as if this were a green-field project: **no
concern with breakage or comms — optimal, unhandcuffed design.** Where a cleaner
design exists, rebuild rather than patch; don't preserve a pattern purely for
backward compatibility. This supersedes prior compatibility hedging, including
the "public shell keeps the amber-border identity *for recognizability*"
framing — the amber-border look stays only where it's genuinely the best design,
not because changing it would break continuity.

**Why.** The audience is ~10–11 known players plus the developer; the impact zone
is tiny, there are no external consumers, and no migration window to protect.
Under those conditions, caution about change is pure drag on entropy reduction.
The mandate is to converge the site's three ad-hoc visual layers into one
coherent system, page by page, without hedging.

**Notes.** "No concern with breakage" means no concern about *changing* things —
not a license to ship broken, ugly, or inaccessible UI. Correctness, taste, and
the verification bar (see `CLAUDE.md`) still hold. The facelift roadmap in
`README.md` now covers the whole site, public pages included, not just staff
tooling.

## 2026-07-11 — Establish the design system + Admin Console language

**Decision.** Stand up `docs/design/` as the living source of truth (this doc,
`tokens.md`, `components.md`, `README.md`), and adopt the **Admin Console**
visual language (`apps/core/static/css/admin-console.css`) as the reference for
staff/admin tooling. The deploy console (`/portal/deploy`) is its first
implementation.

**Why.** The site had grown three ad-hoc visual layers and no written
conventions; a facelift needs a shared vocabulary or it fragments further.

**Notes.** Staff tooling gets the richer layered-grey console look; the public
shell currently keeps the amber-border look. Both share one token/semantic set.
Per the green-field decision above, the amber-border identity is kept only where
it's the best design — public pages are in scope for the same convergence.
Roadmap and enablers in `README.md`.

## 2026-07-11 — Dark-only, forced

**Decision.** The site is dark-only (`<html data-bs-theme="dark">`); no light
theme, no toggle. **Why.** It's the established identity and the game's own
aesthetic; a second theme doubles the surface area for no clear benefit.

## 2026-07-11 — Single amber accent, used sparingly

**Decision.** `#fa7` (`--ishar-color` / `--ac-accent`) is the only brand accent.
Reserve it for brand, focus, primary/live state, and headers — not large fills.
**Why.** One disciplined accent keeps hierarchy legible; spreading amber
everywhere flattens it.

## 2026-07-11 — Fixed semantic color meanings

**Decision.** ok=green `#4cbb17`, info=blue `#4a86cf`, warn=orange `#f80`,
danger=red (`#d64b4b` console / `#d02b2b` classic), immortal=cyan `#00b7eb`.
Same meaning on every surface; never decorative. **Why.** Predictable status
reading across the whole app.

## 2026-07-11 — Bootstrap Icons via the SVG sprite

**Decision.** Prefer `<svg class="bi"><use href="…bootstrap-icons.svg#name">`
over the icon-font classes. **Why.** Inherits `currentColor`, scales cleanly,
and matches the dominant existing pattern.

## 2026-07-11 — No new frontend libraries; self-host

**Decision.** Ship only Bootstrap 5.3.8 + Bootstrap Icons 1.13.1 (self-hosted)
plus small vanilla JS. No new framework, CDN dependency, or web font without a
decision entry. **Why.** Keeps the site fast, offline-buildable, and simple for
a solo maintainer.

## 2026-07-11 — Motion is optional; reduced-motion always honored

**Decision.** Every transition/animation is wrapped by
`@media (prefers-reduced-motion: reduce)`; no motion is load-bearing. **Why.**
Accessibility and taste — the UI must be fully usable and calm without motion.

## 2026-07-11 — JS updates via textContent, not innerHTML

**Decision.** Data-derived DOM updates use `textContent` (and class swaps), never
`innerHTML`. Status pills carry their dot as a `::before` so labels can be
swapped safely. **Why.** Removes an XSS foot-gun class and keeps updates cheap.

---

## Open decisions / to record when made

- **Live styleguide page:** whether to build a staff-only `/styleguide`.
- **Public-shell facelift:** how far the layered-grey console surfaces replace
  the black+amber-outline look on public pages (roadmap #4–#7).
