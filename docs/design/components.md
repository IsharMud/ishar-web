# Component Catalog

The building blocks. Two groups: **de-facto** patterns copy-pasted across the
classic site (formalize these into partials as we go — enabler E2), and the
**Admin Console** components (`.ac-*`), which are the reference for new staff
tooling.

For each: what it is, canonical markup, where it's used, and status.

> Icons everywhere use the sprite:
> `<svg class="bi" aria-hidden="true"><use xlink:href="{% static 'bootstrap-icons/bootstrap-icons.svg' %}#NAME"></use></svg>`

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
`--warn`/`--danger` variants; icon + text. Use for inline warnings/heads-ups.
```html
<div class="ac-note ac-note--warn" role="alert">{# icon #} <span>…</span></div>
```
Status: **formalized.**

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
Admin/portal pages lead with a Portal crumb. Divider is `•`. **Prime candidate
for a partial.**

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
Used in `apps/feedback/templates/feedback_dashboard.html`. **Formalize; the
Admin Console equivalent should become an `.ac-tile`.**

### Filter bar
Row of `btn btn-sm btn-outline-*` toggles (active = solid), driven by Django's
`{% querystring %}` tag, with an inline `role="search"` form. See the feedback
dashboard. Candidate to standardize as `.ac-filter`.

### Contextual badge
`<span class="badge text-bg-{{ status_css }}">{{ status_label }}</span>` with the
color map on the model. On admin surfaces, migrate to `.ac-pill--{ok|info|…}`.

### Empty state
`<div class="card"><div class="card-body"><p class="card-text fst-italic lead
text-warning">No … found.</p></div></div>` (leaders/challenges) — or the feedback
dashboard's `border bg-black card` italic variant. Standardize one.

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
