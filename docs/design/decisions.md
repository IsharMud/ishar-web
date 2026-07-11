# Design Decisions Log

An append-only record of design decisions, newest first. Lightweight ADR: what
we decided, and why. When you make a real design call — a new component, a token
change, a deliberate deviation — add an entry. Don't relitigate settled ones;
supersede with a new dated entry if something genuinely changes.

Format: `## YYYY-MM-DD — Title` · **Decision** · **Why** · (optional) **Notes**.

---

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

- **E1 — shared token base:** where the canonical tokens live (fold `--ac-*` into
  `style.css` vs a new `tokens.css` base include). Record when chosen.
- **E2 — shared components:** the partial/templatetag structure for repeating
  markup (icon, pill, tile, panel header, breadcrumb, empty state).
- **Contextual badges:** migration path from Bootstrap `text-bg-*` to `.ac-pill`
  on admin surfaces (and whether public pages follow).
- **Live styleguide page:** whether to build a staff-only `/styleguide`.
