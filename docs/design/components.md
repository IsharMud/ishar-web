# Component Catalog

The building blocks: the template tags/partials (enabler E2) and the
**console components** (`.ac-*`) — since roadmap #7 these are the whole
site's language, public pages included, not just staff tooling. The old
classic patterns are retired (see the last section).

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

## Console components

Defined in `apps/core/static/css/admin-console.css`, **loaded globally by
`layout.html`** (no per-page include — see decisions.md 2026-07-12).
Reference implementations: `deploy.html` (staff console), `home.html` /
`help_page.html` (public pages), and `/styleguide` live.

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
Uppercase pill; `--muted/--ok/--info/--warn/--danger/--accent/--immortal`
modifiers (`--immortal` is the cyan account-status pill). Add
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
Status: **formalized** (the classic italic-card empty states are gone).

### `.ac-pager` — pagination
Centered `.ac-btn` prev/next around a tabular-nums `.ac-pager__info`;
first/last are icon-only `.ac-btn`s (`chevron-double-*`). Used: news,
patches. Status: **formalized** (supersedes Bootstrap `.pagination`).

### `.ac-timeline` + `.ac-tl` — comment/audit trail
Stacked entries: round source-icon tile, head line (author — `--staff` renders
info-blue — pills, right-aligned time), pre-wrapped text. `--system` entries
recede (deepest surface, dashed border, dim italic text) so human conversation
stays foreground.
Used: feedback detail. Status: **formalized.**

### `.ac-quote` — verbatim text block
Monospace `pre` on the deepest surface with a strong left edge — for captured
player/machine text (report bodies, help-file bodies, game excerpts). The
terminal feel is deliberate. Used: feedback detail, help topics, get-started.
Status: **formalized.**

### `.ac-kv` — key/value details
Two-column `dl` grid; dim keys, right-aligned values. Used: feedback detail.
Status: **formalized.**

### `.ac-link` — navigation card
Anchor sibling of `.ac-toggle`: amber icon tile + name + note, optional
trailing `__side` element (pill/badge). Lay out in `.ac-grid`. Link colors are
pinned against the global `a:link` rule. **`--featured`** marks a first-class
/ officially-supported destination: amber-washed card, amber name — pair it
with a `star-fill` icon tile and an accent pill (e.g. Mudlet's "Ishar
package" card on `/clients`, data-driven via `MUDClient.is_featured` +
`featured_note`).
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

### `.ac-tablewrap` + `.ac-table` — data table
The token-aligned table for **genuinely column-comparable data** (leaderboards);
record lists use `.ac-rows` instead. The wrap owns the border/radius and
scrolls horizontally on phones so the page never overflows. Headers are
uppercase/dim; sortable ones wrap their label in an `.ac-table__sort`
`<button>` — sort state lives on `th[aria-sort]` (arrow via `::after`, amber
when active), applied by a small vanilla-JS sorter (see `leaders.html`).
Numeric cells take `.ac-table__num` (right-aligned, tabular-nums); the rank
column is `.ac-table__rank` (`--top` = amber podium); `.ac-table__sub` is a
dim second line inside a cell (class under player name).
```html
<div class="ac-tablewrap">
  <table class="ac-table">
    <thead><tr>
      <th class="ac-table__num" scope="col" data-type="num">
        <button class="ac-table__sort" type="button">Renown</button>
      </th>
    </tr></thead>
    <tbody><tr>
      <td class="ac-table__num" data-key="4210">4,210</td>
    </tr></tbody>
  </table>
</div>
```
Used: leaders. Status: **formalized** (supersedes the DataTables treatment —
see decisions.md).

### `.ac-row--done` / `.ac-row:target` — row states
`--done` checks a record off: title struck through in ok-green, icon tile
turns ok (challenges). `:target` washes a deep-linked row amber (row `id`s +
fragment links). Status: **formalized.**

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

## Still-live shared patterns (outside `.ac-*`)

### Breadcrumb item — `{% crumb %}`
Every page's title line. Use the tag (see above); no template hand-writes
crumb markup anymore.

### `<details>/<summary>` section
Collapsible with an amber `summary` (`.h5 text-ishar`) + `.anchor-link` "#"
affordance, inside an `.ac-panel`. Used: FAQ. Fine to reuse where content is
genuinely collapsible; don't use it as a section header substitute.

### Global nav "Portal" dropdown
`apps/core/templates/layout.html` — the staff/admin menu (Administration,
Deploy, Feedback Triage, …), gated by `is_staff`/`is_god`/`is_eternal`. The
canonical place to surface a new staff tool (mirror the existing items).
Count badges in the nav are plain `.ac-pill`s.

---

## Retired classic patterns (roadmap #7 — do not reintroduce)

Gone from live templates and (where they had CSS) from `style.css`:

- **Black+amber panel** (`bg-black border-ishar rounded`), Bootstrap
  `.card`/`.list-group` stacks → `.ac-panel` / `.ac-rows`.
- **Count pill** (`badge bg-dark rounded-pill border-secondary`) → `.ac-pill`.
- **Stat tile** (`display-6` card) → `.ac-tile`.
- **Filter bar** (`btn-outline-*` toggles) → `.ac-filter` + `.ac-chip`.
- **Contextual badge** (`badge text-bg-*`) → `.ac-pill--*` (color map stays on
  the model, e.g. `Feedback.status_pill`).
- **Empty state** (italic warning card) → `.ac-empty`.
- **DataTable** (jQuery DataTables) → `.ac-table` (leaders) / filterable
  `.ac-rows` (upgrades); the vendored `datatables/` + `jquery-3.7.1` assets
  are deleted.
- **Bootstrap `.pagination`** → `.ac-pager`.
- **Dismissible `alert-dark` info boxes** on static content → hero subs,
  panel prose, or `.ac-note`.
- **Tooltips/popovers for help text** → `.ac-panel__hint` prose (portal
  decision, applied site-wide).

---

## Connect HUD components (page-specific, `apps/connect/static/css/hud.css`)

The browser client's widget layer. Page-specific by design (it only loads on
`/connect`), but it draws every color from the shared tokens and follows the
same conventions (radii, focus, coarse-pointer, reduced-motion). Highlights:

- **Layout modes** — desktop: collapsible `#hud-left` / `#hud-right` columns
  (`.l-closed` / `.r-closed` on `#connect-app`, persisted) around a
  priority-width terminal; phone: terminal-first with `#hud-dock` (bottom tab
  bar) + `#hud-sheet` (one-panel bottom sheet). `hud.js` re-parents the panel
  sections between the columns and the sheet on the 768px media-query flip.
- **`.panel` / `.panel-h`** — the HUD's compact panel + uppercase header
  (denser cousins of `.ac-panel` / `.ac-panel__h`).
- **`.vbar` / `.mini`** — labeled vitals bars (HP/MP/MV/Foe/XP/MM/Edge) and
  the tiny group-member triple.
- **`.hud-btn`(`--icon`)** — the topbar button, aligned with `.ac-btn`.
- **`#hud-dock button`** — icon-over-label phone tabs; `.unread` renders an
  amber dot (used by Chat).
- **`.exit` compass, `.row` lists, `.kv`, `.aff`, `.skill` hotbar** — the
  in-panel widgets; all have coarse-pointer bumps and `:focus-visible` rings.

Verify with `/connect?demo=1` (sample GMCP feeds, no server needed).

---

## When adding a component

1. Check this catalog first — extend, don't fork.
2. Name it `.ac-*`, define it in `admin-console.css`, key it off tokens
   (tokens.md), and guard any motion with `prefers-reduced-motion`.
3. Add it here with markup + status, and log the decision in `decisions.md`.
