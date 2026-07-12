# Component Catalog

The building blocks. Two groups: **de-facto** patterns copy-pasted across the
classic site (formalize these into partials as we go — enabler E2), and the
**Admin Console** components (`.ac-*`), which are the reference for new staff
tooling.

For each: what it is, canonical markup, where it's used, and status.

> Icons everywhere use the sprite:
> `<svg class="bi" aria-hidden="true"><use xlink:href="{% static 'bootstrap-icons/bootstrap-icons.svg' %}#NAME"></use></svg>`

---

## Template tags & partials (`{% load ishar %}`)

Enabler E2 — defined in `apps/core/templatetags/ishar.py`, partials under
`apps/core/templates/partials/`. Use these in any new/touched template instead
of pasting the markup.

### `{% bi %}` — sprite icon
```django
{% bi "rocket-takeoff" %}                              {# decorative (aria-hidden) #}
{% bi "lock-fill" css="text-warning" label="Private" %} {# meaningful (role=img) #}
```
Output is built with `format_html` (labels are escaped). Status: **formalized.**

### `{% crumb %}` — breadcrumb item
```django
{% crumb "Portal" "person-gear" urlname="portal" anchor="portal" %}
{% crumb "Deploy" "rocket-takeoff" urlname="deploy" anchor="deploy" active=True %}
```
Reverses `urlname` (+ `#anchor`), puts `id="{{ anchor }}"` on the label span so
`focusTo` deep-linking works, sets `aria-current` when active. Omit `urlname`
for an unlinked crumb. Status: **formalized.**

---

## Admin Console components

Defined in `apps/core/static/css/admin-console.css`; load per page via
`{% block includes %}`. Reference implementation:
`apps/accounts/templates/deploy.html`.

### `.ac-hero` — page header banner
Gradient + 3px amber left edge, circular badge, title, subtitle, optional status
pill on the right.
```html
<header class="ac-hero">
  <span class="ac-hero__badge">{# icon #}</span>
  <div class="ac-hero__text">
    <h2 class="ac-hero__title">Deploy Console</h2>
    <p class="ac-hero__sub">Short description with <code>code</code>.</p>
  </div>
  <div class="ac-hero__status">{# an .ac-pill #}</div>
</header>
```
Status: **formalized.** Use as the top of any admin page.

### `.ac-pill` — status pill
Uppercase pill; `--muted/--ok/--info/--warn/--danger/--accent` modifiers. Add
`.ac-pill--status` to get a leading dot (a `::before`, so JS may swap the label
via `textContent`), and `.ac-pill--live` to make that dot pulse.
```html
<span class="ac-pill ac-pill--status ac-pill--ok ac-pill--live">agent online</span>
```
Status: **formalized.** This is the site's status-badge going forward
(supersedes ad-hoc Bootstrap `badge bg-*` on admin surfaces).

### `.ac-panel` + `.ac-panel__h` — section panel
Bordered panel with an uppercase dim header (optionally an amber icon) and an
optional `.ac-panel__hint`.
```html
<div class="ac-panel">
  <div class="ac-panel__h">{# icon #} Environment</div>
  <p class="ac-panel__hint">Helper text.</p>
  …
</div>
```
Status: **formalized.**

### `.ac-seg` — segmented control
Pill group of mutually exclusive options over hidden `.btn-check` radios (keeps
`input[name=…]:checked` working). Intent tints via `--prod`/`--test`-style
modifiers.
```html
<div class="ac-seg" role="radiogroup">
  <input class="btn-check" type="radio" name="env" id="env-prod" checked>
  <label class="ac-seg__item ac-seg__item--prod" for="env-prod">{# icon #} prod</label>
  …
</div>
```
Status: **formalized.**

### `.ac-toggle` — selectable card
Checkbox styled as a card (icon tile + name + note + check indicator), over a
hidden `.btn-check`. Selected state uses the amber wash.
```html
<input class="btn-check" type="checkbox" name="services" id="svc-x">
<label class="ac-toggle" for="svc-x">
  <span class="ac-toggle__icon">{# icon #}</span>
  <span class="ac-toggle__body">
    <span class="ac-toggle__name">svc-x</span>
    <span class="ac-toggle__note">what it is</span>
  </span>
  <span class="ac-toggle__check">{# check-circle-fill #}</span>
</label>
```
Lay out in `.ac-grid` (responsive auto-fit). Status: **formalized.**

### `.ac-switch` — labeled switch
Bootstrap `form-check form-switch` recolored amber. Status: **formalized.**

### `.ac-inputgroup` / `.ac-input` — icon input
Input with a leading icon cell; focus ring is the amber wash.
```html
<div class="ac-inputgroup">
  <span class="ac-inputgroup__icon">{# key #}</span>
  <input class="ac-input" type="password" placeholder="…">
</div>
```
Status: **formalized.**

### `.ac-cta` — primary/destructive button
Gradient button; `.ac-cta--ready` adds a gentle armed glow. Status:
**formalized** (destructive/red today; add an accent variant when a
non-destructive primary is needed).

### `.ac-console` — job/log terminal
Header bar with faux traffic-lights, a title, an `.ac-pill` status, a
`tabular-nums` timer, and a copy button; an optional `.ac-console__step` row (a
spinner + a headline parsed from `==>` lines); a monospace `.ac-console__body`
log. Status: **formalized.** Use for any long-running job with streamed output.

### `.ac-note` — callout
`--ok`/`--warn`/`--danger` variants; icon + text. Use for inline
warnings/heads-ups and JS-swapped action results (`textContent` + class swap).
```html
<div class="ac-note ac-note--warn" role="alert">{# icon #} <span>…</span></div>
```
Status: **formalized.**

### `.ac-tiles` + `.ac-tile` — KPI stat tiles
Grid of clickable count tiles that double as filters. Semantic number color via
`--ok/--info/--warn/--danger/--accent`; pass `--muted` when the count is zero
so only live numbers draw the eye; `--active` marks the currently-applied
filter.
```html
<div class="ac-tiles">
  <a class="ac-tile ac-tile--danger ac-tile--active" href="?flag=unacked">
    <span class="ac-tile__n">3</span>
    <span class="ac-tile__label">Unacknowledged</span>
  </a>
</div>
```
Used: feedback dashboard. Status: **formalized** (supersedes the classic
`display-6` card tile on admin surfaces).

### `.ac-filter` + `.ac-chip` — filter bar
Wrapping rows of pill chip links (one row per dimension, `.ac-filter__sep` as a
group divider); active chip gets `--active` (amber wash). Compose with an inline
`role="search"` form of `.ac-field`s. Driven by `{% querystring %}`.
```html
<div class="ac-filter" role="group" aria-label="State filter">
  <a class="ac-chip ac-chip--active" href="…">Active</a>
  <a class="ac-chip" href="…">Closed</a>
</div>
```
Used: feedback dashboard. Status: **formalized.**

### `.ac-btn` — secondary action button
Small, bordered action button (the page's one primary stays `.ac-cta`).
Semantic variants `--ok/--info/--warn/--danger/--accent` color text/border and
fill the matching wash on hover. Works on `<a>` too (link colors are pinned).
```html
<button class="ac-btn ac-btn--ok" data-action="ack">Ack</button>
```
Status: **formalized.**

### `.ac-field` + `.ac-label` — bare form field
Input/textarea/select without the icon cell (`.ac-inputgroup` is the icon
variant). `--inline` for auto width. `.ac-label` is the uppercase dim label.
Status: **formalized.**

### `.ac-rows` + `.ac-row` — record list
The console list surface (mobile-first replacement for data tables — see
decisions.md): one bordered stack; each row is wrapping flex with an icon tile
(`__icon`), a main cell (`__title` with an `a.ac-row__link`, then a `__meta`
line), and a right-aligned `__side` for pills/actions.
```html
<div class="ac-rows">
  <div class="ac-row" id="row-7">
    <span class="ac-row__icon">{% bi "bug" %}</span>
    <div class="ac-row__main">
      <div class="ac-row__title"><a class="ac-row__link" href="…">Summary</a></div>
      <div class="ac-row__meta"><span class="mono">#7</span> <span>Reporter</span></div>
    </div>
    <div class="ac-row__side">{# .ac-pill, .ac-btn #}</div>
  </div>
</div>
```
Used: feedback dashboard. Status: **formalized.**

### `.ac-empty` — empty state
Dashed, centered, dim: icon + one sentence.
```html
<div class="ac-empty">{% bi "inbox" %} <span>No reports match.</span></div>
```
Status: **formalized** (supersedes the classic italic-card empty states as
pages are touched).

### `.ac-pager` — pagination
Centered `.ac-btn` prev/next around a tabular-nums `.ac-pager__info`. Status:
**formalized.**

### `.ac-timeline` + `.ac-tl` — comment/audit trail
Stacked entries: round source-icon tile, head line (author — `--staff` renders
info-blue — pills, right-aligned time), pre-wrapped text. `--system` entries
recede (deepest surface, dashed border, dim italic text) so human conversation
stays foreground.
Used: feedback detail. Status: **formalized.**

### `.ac-quote` — verbatim text block
Monospace `pre` on the deepest surface with a strong left edge — for captured
player/machine text (report bodies, pasted output). The terminal feel is
deliberate. Status: **formalized.**

### `.ac-kv` — key/value details
Two-column `dl` grid; dim keys, right-aligned values. Used: feedback detail.
Status: **formalized.**

### `.ac-link` — navigation card
Anchor sibling of `.ac-toggle`: amber icon tile + name + note, optional
trailing `__side` element (pill/badge). Lay out in `.ac-grid`. Link colors are
pinned against the global `a:link` rule.
```html
<a class="ac-link" href="…">
  <span class="ac-link__icon">{% bi "flag" %}</span>
  <span class="ac-link__body">
    <span class="ac-link__name">Feedback Triage</span>
    <span class="ac-link__note d-block">Player bug / typo / idea reports</span>
  </span>
  <span class="ac-link__side ac-pill ac-pill--ok">4</span>
</a>
```
Used: portal tool grids. Status: **formalized.**

### Container variants
`.ac` (60rem) is the default console width; `.ac--wide` (72rem) for list-heavy
surfaces. `.ac-cta--accent` is the amber non-destructive primary (red stays
destructive).

---

## Shell components (global frame, `style.css`)

- **`.shell-panel`** — the frame surface (nav, messages, `#content`, footer,
  search): `--ac-panel` bg, `--ac-border` hairline, `--ac-radius`. The navbar
  variant adds a 2px amber bottom edge.
- **`.shell-menu`** — dropdown menus: `--ac-elev` bg, `--ac-border-2` hairline,
  small radius.
- **Breadcrumbs** are a quiet page-title line (no box); h2-sized crumbs from
  old templates are downsized by CSS. Crumb/nav icons are amber; footer icons
  dim.

---

## Classic / de-facto patterns (formalize into partials)

These are copy-pasted across templates today. Catalogued so we can extract them
into `{% include %}` partials / template tags (E2) and, later, restyle once.

### Panel (classic)
`<div class="bg-black border-ishar my-1 p-2 rounded">` — the universal black +
amber-outline container (`#content`, footer, messages, search form). The classic
site's card idiom.

### Breadcrumb item
Every page reimplements:
```html
<li class="breadcrumb-item h2" title="…">
  <a class="icon-link icon-link-hover" href="…">{# icon #} <span>Label</span></a>
</li>
```
Admin/portal pages lead with a Portal crumb. Divider is `•`. **Formalized as
`{% crumb %}` (see above) — use the tag; migrate old templates as touched.**

### Count pill
`<span class="badge bg-dark rounded-pill border border-secondary">{{ n }}</span>`
— the standard "stat count" chip (events, players-online, essence, upgrades).

### Stat / KPI tile
The feedback dashboard's clickable tile — big number + uppercase secondary label,
semantic number color, zero-suppressed emphasis:
```html
<a class="text-decoration-none" href="?filter=…">
  <div class="border bg-black card text-center p-2 h-100">
    <span class="display-6 {% if n %}text-danger{% endif %}">{{ n }}</span>
    <span class="text-secondary small text-uppercase">Label</span>
  </div>
</a>
```
**Superseded on admin surfaces by `.ac-tile` (see above);** the classic markup
survives only on untouched pages.

### Filter bar
Row of `btn btn-sm btn-outline-*` toggles (active = solid), driven by Django's
`{% querystring %}` tag, with an inline `role="search"` form. **Superseded by
`.ac-filter` + `.ac-chip` (see above).**

### Contextual badge
`<span class="badge text-bg-{{ status_css }}">{{ status_label }}</span>` with the
color map on the model. **On admin surfaces this is now `.ac-pill--{{
status_pill }}`** — the model carries both maps (see `Feedback.status_pill` and
decisions.md); classic badges survive only on untouched pages.

### Empty state
`<div class="card"><div class="card-body"><p class="card-text fst-italic lead
text-warning">No … found.</p></div></div>` (leaders/challenges). **Superseded by
`.ac-empty` (see above)** as pages are touched.

### DataTable
`table table-hover table-dark table-flush table-sm table-responsive
table-striped` with `text-ishar` headers + `table-group-divider`. Used on
leaders & challenges (needs the DataTables include). Keep, but align header/hover
colors to tokens.

### `<details>/<summary>` section
Collapsible with an `.anchor-link` "#" affordance + `h3/h4/h5` + count badge —
the portal's section pattern.

### Global nav "Portal" dropdown
`apps/core/templates/layout.html` — the staff/admin menu (Administration,
Deploy, Feedback Triage, …), gated by `is_staff`/`is_god`/`is_eternal`. The
canonical place to surface a new staff tool (mirror the existing items).

---

## When adding a component

1. Check this catalog first — extend, don't fork.
2. Name it `.ac-*`, define it in `admin-console.css`, key it off tokens
   (tokens.md), and guard any motion with `prefers-reduced-motion`.
3. Add it here with markup + status, and log the decision in `decisions.md`.
