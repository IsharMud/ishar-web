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
{% url 'survey_results' survey.slug as results_url %}{% crumb "Results" "bar-chart" url=results_url %}
```
Reverses `urlname` (+ `#anchor`), puts `id="{{ anchor }}"` on the label span so
`focusTo` deep-linking works, sets `aria-current` when active. For routes that
need arguments, pass a prebuilt `url=` instead of `urlname`. Omit both for an
unlinked crumb. Status: **formalized.**

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

### `.ac-opts` + `.ac-opt` — option rows
`.ac-toggle`'s lighter sibling for long radio/checkbox lists (survey answers):
a compact row over a hidden `.btn-check`, with a drawn `__mark` disc that
fills amber when checked. `--box` squares the mark for checkboxes.
`.ac-opt-other` pairs a pick with its "Other: ___" `.ac-field` on one
wrapping row (the field enables with the pick, via JS).
```html
<div class="ac-opts">
  <input class="btn-check" type="radio" name="q1" id="q1-o1" value="1">
  <label class="ac-opt" for="q1-o1"><span class="ac-opt__mark" aria-hidden="true"></span>0–5</label>
  …
</div>
```
Used: survey form. Status: **formalized.**

### `.ac-q` — question block
One survey/form question inside an `.ac-panel`: `__text` (with an amber
mono `__num`), optional `__hint`, an `__error` line, `--invalid` danger left
edge. Siblings separate with a dashed rule. Companions: `.ac-mx`/`.ac-mx__row`
(matrix rows — an `.ac-label` over an `.ac-seg--wrap` rating segment) and
`.ac-rank` (labeled ordinal `.ac-field` selects in a responsive grid).
Used: survey form + results. Status: **formalized.**

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

### `.ac-bars` + `.ac-bar` — single-series magnitude bars
Server-rendered horizontal bar rows: label · track+fill · value. One hue per
group (`--ac-info` default; `.ac-bar--accent` for a second *group* on the same
panel, never per-row rainbow); identity lives in the row label, the value in a
text token at the tip — the fill is the only colored ink. Width is a
server-computed percentage of the group's max. Rounded data-end, square
baseline. Pair with a table when the data deserves exact columns.
```html
<div class="ac-bars">
  <div class="ac-bar" title="12 accounts: today">
    <span class="ac-bar__label">Today</span>
    <span class="ac-bar__track"><span class="ac-bar__fill" style="width: 100%;"></span></span>
    <span class="ac-bar__n">12</span>
  </div>
</div>
```
Used: staff dashboard. Status: **formalized.**

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
  The left column stacks **Group · Here** above the pinned Room/rose; the
  right column is **Tracked Spells over Chat** — no tab bar. Reference surfaces
  (Gear, **Bags**, Character, Abilities, Who) are overlay apps, not columns/tabs
  (see the overlay section below and decisions.md 2026-07-19).
- **`.panel` / `.panel-h`** — the HUD's compact panel + uppercase header
  (denser cousins of `.ac-panel` / `.ac-panel__h`).
- **`.vbar` / `.mini`** — labeled vitals bars (HP/MP/MV/Foe/MM/Edge) and
  the tiny group-member triple. (XP is no longer a `.vbar` — it graduated to the
  ambient `#hud-xpstrip`; see below.)
- **`.vbar-reserve`** — the hunger (`.food`, apple) / thirst (`.water`, droplet)
  icon riding the end of the HP and MV bars; `data-state` `ok`/`low`/`crit`
  tints it dim → `--hud-edge` → `--ac-danger`. Built client-side via `biSvg()`
  from `Char.Vitals.food`/`water` (see decisions.md 2026-07-17).
- **`.v-affects` / `.self-aff`** — the ambient self buff/debuff strip by the
  vitals (`#vitals-affects`, `renderSelfAffects`). Bare 26px icon tiles, buff
  green / debuff red; a `.self-aff-chip` countdown + an `.alarm` pulse appear
  only within `AFFECT_SOON` (60s) of expiry, so ~10 buffs stay a compact
  wrapping row. From `Char.Affects.buffs`/`.debuffs` (see decisions.md
  2026-07-18, "HUD affects split").
- **`#hud-xpstrip`** — the ambient XP strip below the terminal (between it and
  `#hud-actionrow`). A **5px hairline**: a `.xp-track` (`flex:1`) holding the
  `.xp-fill` (`--hud-xp` violet, width = `Char.Train.xp_pct`), with the
  `.xp-label` caption sitting **beside** it (not baked in) — `XP <pct>% · to
  L<next>` (`Char.Status.level + 1`), the `.xp-pct` tinted `--hud-xp`.
  `renderXp()` swaps the fill width + rebuilds the caption; `hidden` until
  `Char.Train` arrives, and hidden in `.hud-off`. Ambient on phones too (the
  bar shrinks, the caption stays at 390px). See decisions.md 2026-07-19,
  "HUD XP strip" and its refinement note.
- **`.hud-btn`(`--icon`)** — the topbar button, aligned with `.ac-btn`.
- **`#hud-dock button`** — icon-over-label phone tabs; `.unread` renders an
  amber dot (used by Chat), `.alarm` a pulsing caution dot (used by Tracked
  Spells when a maintained spell nears expiry).
- **`.exit` compass, `.item-row` lists, `.kv`** — the in-panel widgets;
  all have coarse-pointer bumps and `:focus-visible` rings.
- **`.grp` (Group)** — the party pane in the left column (`#panel-group`,
  `renderGroup`), with two density presets a header toggle (`.grp-dens`,
  persisted `ishar.groupDensity`) flips between — **not** a field-picker.
  **Full** (default) is the rich row: `.grp-main` with name · triage-tinted
  `.grp-hp-num` % · `.grp-chips` (`.grp-tank` / `.grp-threat` / `.grp-fight` /
  `.grp-pos` / `.grp-away`) · the `.grp-bars` HP/MP/MV `.mini` triple, in feed
  order. **Compact** (`.grp-cmp`, `groupRowCompact`) is one scannable line —
  `.grp-cn` name · `.grp-cbar` triage-tinted HP bar · `.grp-cp` % · a single
  `.grp-ct` status marker (`.mark-cc` amber for stunned/fleeing/asleep, `.mark-tank`
  red) · `.grp-range` `away` — sorted low-HP/tank-first and capped to `44vh`
  in-column scroll (`.grp-cmp-list`); the whole row is the tap target (`data-menu`,
  no `⋯`). Tank rows keep the `.tanking` left border in both. From `Group.Update`;
  see decisions.md 2026-07-19 (HUD Group density).
- **`.aff` (Tracked Spells)** — one row per maintained spell in the persistent
  right-column `#panel-tracked` (`renderTracked`): `.aff-ic` icon · `.aff-body`
  (name + colour-coded `.aff-tgt` `self`/`mate`/`foe`) · `.aff-time` · `.aff-rel`
  release button. Expiry-sorted; `.aff.soon` warms a row nearing expiry. From
  `Char.Affects.maintained`.
- **`.panel-chat` (Chat)** — the second persistent right-column pane (dock sheet
  on phones), `renderChat`. A collapsible `panelHeader` over three parts: a
  **`.chat-tabs`** segmented filter (`All / Public / Tells / Group`,
  single-select, persisted `ishar.chatFilter`), the scrolling **`.chat-log`**,
  and a **`.chat-in`** channel-targeted input (a `.chat-ch-select` over a
  `.chat-msg` field; pick a channel, type, Enter routes `<verb> <text>` without
  the verb, persisted `ishar.chatChannel`). Each `.chat-line` leads with a
  `.chat-ch` tag tinted by category (`.ch-public` amber / `.ch-tells`
  `--hud-mm` / `.ch-group` `--hud-group`); the game's redundant `[World] ` text
  prefix is stripped. From `Comm.Channel` (`channel` label + rendered `text`);
  see decisions.md 2026-07-19 (HUD Chat) for the real channel taxonomy.
- **`.item-row`** — the equipment/inventory row (NB: **not** `.row` — that's
  Bootstrap's grid class, loaded globally; see decisions.md). One nowrap flex
  line: an optional lead cell (a `.row-caret` on an expandable container, else
  a `.cond-dot`), `.row-name` (ellipsized), a `.tag` ×count, an optional
  `.row-glyph` (🔒/📦) for a closed container, and the trailing `.row-more` ⋯.
  Item condition is a **colour-coded `.cond-dot`** (● ok/mid/low, exact % in
  the `title`), never a word on its own line. Worn containers expand inline
  to a `.row-list.sub`; **packs start collapsed** and toggle via the caret
  (`data-expand`, persisted in `ishar.itemsExpanded`). Identical stackable
  rows are folded to one `×N` (the game emits duplicate rows; the HUD
  defaults to stacking). A consumable row carries an inline **`.item-pin`**
  `☆/★` chip (`data-pin`) that pins/unpins it on the action bar.
- **`.bag` (Bags overlay)** — the aggregated worn + carried storage view
  (`renderInventory`, the `inventory` overlay app, title "Bags"). Leads with
  container **cards**: a `.bag-h` header (its own open/close/get-all menu) with
  a `.bag-ic` glyph, `.bag-nm` name, a `.bag-prov` provenance tag (`carried`, or
  `.worn` amber for `worn: <slot>`), and a `.bag-lock` note when locked; over its
  contents (`.item-row`s) or a `.bag-items li.dim` "locked/closed/empty" note.
  Then a **Loose in inventory** `.sub-h`, the Components pouch, and coins. From
  `Char.Equipment` (worn containers) + `Char.Inventory`. See decisions.md
  2026-07-19 (Bags overlay + item pinning).
- **`.skill` action bar** — the WoW-style bottom hotbar (`#hud-hotbar`): fixed,
  numbered, hotkey-addressable icon slots. Each `.skill` is a square holding a
  `.skill-icon` (a Game-Icons.net glyph, below), a `.skill-key` number badge,
  a `.skill-cd` cooldown/blocked overlay, and a `.skill-sweep` radial wedge
  (`--sweep` angle, motion-gated). School tints via `.cat-*`; states via
  `.off`/`.cooling`/`.blocked`/`.sweeping`/`.fired`/`.dragging`/`.drop-target`.
  `.skill--empty` is a numbered drop target, `.skill--pager` the 1/2 page
  toggle, `.skill--lock` the lock/unlock. A slot can also hold a **pinned item**
  (`.skill--item`, gold accent): a consumable's keyword command, a type-picked
  glyph, and a live `.skill-count` corner badge that greys the tile (`.off`) at
  zero stock (count by vnum against `Char.Inventory`). Slots persist in
  `ishar.slots` (ordered; skills are strings, items `{item,cmd,vnum,otype,name,
  icon}`; migrated from the old `ishar.favs`); per-skill icon overrides in
  `ishar.icons`; the unlocked state in `ishar.barUnlocked`. See the 2026-07-16
  and 2026-07-19 decisions. Hotkeys: **Alt/Ctrl+1…0** fire, **Alt+`** pages.
  **Locked by default** (taps fire); unlock to edit — `#hud-hotbar.editing` gets
  grab cursors and a `.skill.picked` slot awaits its destination (tap-to-swap).
- **Game-Icons.net sprite** (`img/game-icons.svg`, CC BY 3.0, self-hosted) —
  the **skill-art** vocabulary, a scoped exception to the Bootstrap-Icons-only
  rule (see decision). Referenced like `bi` but with class `gi`:
  `<svg class="gi"><use href="{% static 'img/game-icons.svg' %}#gi-NAME"></use></svg>`
  (hud.js builds these with `createElementNS` + a sanitized href). Glyphs are
  single-path `currentColor`, so they recolor by school. Bootstrap Icons stays
  the sprite for everything else.
- **Standardized skill→icon map** — the icon a skill gets is resolved
  personal pick → server-provided → curated map → keyword heuristic. The curated
  map (`apps/connect/skill_icons.py`, keyed by normalized skill name, **all 462
  skills mapped**) is injected via `{{ skill_icons|json_script:"ishar-skill-icons" }}`
  and `IsharHUD.init({skillIcons})`; it's the standardized default everyone
  inherits. Regenerate from `python manage.py dump_skills` + the heuristic. See
  the 2026-07-16 decision (incl. the future game-side `icon` field).
- **`.hud-tip` tooltip** — the HUD's single hover/focus tooltip convention.
  **Terse by rule:** a bold `.tip-name`, an optional right-aligned `.tip-key`
  chip (the hotkey), and at most one `.tip-sub` line (`.tip-warn` red-tokens a
  block reason). Opt in with `data-tip="text"` on any element; the action bar
  supplies structured tips. Hover + keyboard focus, hover-capable pointers only
  (touch uses the long-press menu); fade gated behind reduced-motion. One shared
  `#hud-tip` node, built in `hud.js`.
- **`.picker-grid` / `.picker-icon` / `.picker-auto`** — the per-skill icon
  picker (a themed grid reusing `#hud-menu.menu-picker`); opened from an
  ability's context menu. `.ab-icon` mirrors the chosen glyph in the Abilities
  list, and the `☆/★` `.ab-star` (data-bar) pins to the action bar.
- **`#history-pop` / `.hist-item`** — the touch command-history popover,
  anchored above the input inside `#command-form` (works with the HUD off;
  rows are `textContent`-built, 44px on coarse pointers). Revealed via
  `#history-btn`, which JS un-hides on `(pointer: coarse)`.
- **`#settings-pop` / `.setting-row`** — the gear menu under the topbar's
  right edge: checkbox rows persisted in `ishar.settings`, mirrored by the
  `/settings` client command.
- **`#term-search`** — the scrollback find bar floating over the terminal's
  top-right (input + prev/next/close); opened by `#search-btn` or
  Ctrl+Shift+F, closed by Esc. Match decorations use the amber accent.
- Note `.hud-btn[hidden] { display: none; }` — the button's explicit
  `display` would otherwise defeat the `hidden` attribute.
- **`#hud-actionrow` / `#hud-micro` / `.micro-btn`** — the action row wraps
  the skill bar plus the **micro-menu**: small icon buttons (32px, `{% bi %}`
  glyphs) that toggle transient **overlay apps** (`Ctrl`+letter hotkeys; see
  decisions.md "The HUD extension model", 2026-07-17). Launchers are
  availability-gated by their feed (`hidden` when there's nothing to show) and
  may carry a `.unread` dot (feed changed while closed) and a `.micro-strip`
  progress bar (long-running activity). Hidden on phones — the dock is the
  phone's micro-menu.
- **`#hud-overlay` / `.overlay-head` / `.overlay-title`** — the desktop
  overlay window (fixed, centered, `z-index` 1038 — above sheet/popovers,
  below `#hud-menu`): one `.panel.overlay-active` at a time from
  `#hud-overlay-body`; dismissed by Esc, outside-click, ✕, the hotkey or the
  launcher. On phones the same panel node opens in `#hud-sheet` via a dock
  button (`placePanels()` re-homes it). Register apps in the `OVERLAYS`
  table in `hud.js`.
- **Reference overlay apps** (`OVERLAYS` keys `inventory`/`train`/`abilities`/
  `who`, migrated out of the columns + right-column tab bar — decisions.md
  2026-07-19): **Bags** (`renderInventory`, the `.bag` aggregation above),
  **Character** (worn gear + stats in one overlay — decisions.md 2026-07-19
  "Character overlay merge"), **Abilities** (`renderAbilities`, the `.ab-*`
  browser below), and **Who** (`renderWho`, `.who-list`). Each renders **bare**
  (the window/sheet chrome supplies the title — no in-panel `panelHeader`) and is
  availability-gated on its feed, so its micro + dock launchers appear only once
  there's data. Hotkeys Ctrl+I/K/B/U.
- **`.char-cols` Character overlay** — one overlay (`train`, Ctrl+K, person icon)
  holding two fill targets inside `#panel-train`: `#char-gear` (`renderEquipment`,
  worn `.item-row`s in wear-slot order) and `#char-stats` (`renderTrain` —
  stats/resources/aux `.kv` + the folded-in `Char.Status` reference kv). Each
  column is headed by a `.char-h` label ("Worn" / "Stats"). Two columns with a
  divider on desktop (`#hud-overlay[data-app="train"]` widens to 720px), stacked
  in the phone sheet — `grid-template-columns: minmax(0, 1fr)` so long gear names
  ellipsis instead of forcing the panel wide. Available when either
  `Char.Equipment` or `Char.Train`/`Char.Status` has data. There is no separate
  Gear/Equipment overlay, no Status panel, and XP lives in the ambient
  `#hud-xpstrip`, not here.
- **`.ab-*` Abilities browser** (`.ab-controls/.ab-search`, `.ab-chips/.ab-chip`,
  `.ab-scroll/.ab-list/.ab-row`, `.ab-name/.ab-right/.ab-block/.ab-pct/.ab-star/
  .ab-type`) — the searchable, type-filtered, usable-only skill list fed by
  `Char.Skills`. The search box + filter chips **pin** (`position: sticky`) to
  the top of the scroll container — the overlay body on desktop, the dock sheet
  on phones (one CSS rule serves both) — so a 400-row list never scrolls the
  controls away. Rows carry the school `.cat-*` left border, the `☆/★` pin, and
  a `⋯` action menu.
- **Professions app** (`.prof-row/.prof-head/.prof-track/.prof-btn`,
  `.recipe-list/.recipe-cat/.recipe-row`,
  `.craft-activity/.craft-track/.craft-fill/.craft-time`) — the reference
  overlay app: profession standing rows (disclosure header + tier `.tag` +
  `Rank n/max` + rank meter + recipe counts) fed by `Char.Professions`,
  topped by the live craft/harvest cast bar fed by `Char.Craft` (ticked
  locally each second; the micro button mirrors it as `.micro-strip`).
  Expanding a row opens the **recipe browser** fed by `Char.Recipes`
  (`.recipe-controls/.recipe-search/.recipe-chips/.recipe-chip`,
  `.recipe-cat/.recipe-cat-caret/.recipe-cat-name/.recipe-cat-count`,
  `.recipe-row/.recipe-toggle/.recipe-name/.recipe-rank/.recipe-avail`,
  `.recipe-comps`, `.recipe-queue/.recipe-qty-btn/.recipe-qty-num`):
  - **Controls.** A per-profession **search** box plus filter chips — an
    **Available** toggle (craftable-now only, persisted) and one chip per
    **category** — share the abilities overlay's `.ab-search`/`.ab-chip`
    styling (one CSS rule serves both).
  - **Categories** are collapsible **section headers** (a thematic-break
    rule, caret, name, count), ordered **by paperdoll slot — head → feet,
    with the held items (weapon/shield) in their worn position (below
    hands, above the waist) — then unknown categories alpha, with
    transmutation / general last** — *not* the game's alphabetical order
    (a deliberate web presentation choice; see the ADR).
  - **Rows.** Name colored by the **`.tier-*` difficulty classes**
    (trivial/easy/medium/hard/blocked — computed client-side from
    `min_rank` − rank), a **bare rank number** (`.recipe-rank`, no `r`
    prefix), and a **craftable-count badge** (`.recipe-avail`): green
    `×N` (how many the carried components allow — mirrors the game's
    `recipe_available_count`), `✓` (ready / targeted), or red `Missing`.
    Action per row: **Craft** (targetless; hidden while the row's detail
    is open) or **Enchant…** (targeted — an item picker over carried
    items whose `gear_type` matches `target_gear_type`, sending
    `enchant <item> <recipe>`).
  - **Detail** (tap the name) discloses `.recipe-comps` — the per-component
    have/need breakdown (the touch path to "what am I missing?") — and, for
    targetless recipes, the **batch-craft queue** (`.recipe-queue`): a
    keyboard-free `−`/`+` stepper + editable count + **Max** (= components
    on hand) + **Craft ×N**, sending `<verb> <recipe> <count>` (the game's
    craft chain, capped at 99).
  The `.tier-*` classes also color the enchanter's **`Disenchant (rN)`**
  entry in inventory item context menus (from the item's
  `disenchant_rank`). Note one deliberate palette divergence: the trivial
  tier renders `--ac-dim` (de-emphasis) where the game shows white —
  worthless-for-skillup recipes should recede, not match body text.

- **Map (Rose | Map tabs, minimap, overlay app)** — the fog-of-war world map
  (`hud-map.js`, isharmud/ishar-web#125). `.rose-tabs` turns the pinned Room
  panel header into a Rose | Map micro-tab pair (persisted `ishar.roseTab`;
  `.rose-expand` ⤢ opens the big map). `.map-mini` hosts the minimap canvas
  (~7×7 cells centered on the player; tap an adjacent room to walk, tap
  farther for the room menu); `.map-hint` is the "location unknown" veil
  when the player can't see. The **overlay app** (`OVERLAYS` key `map`,
  `Ctrl+M`; `#hud-overlay[data-app="map"]` widens the window) is
  `.map-app` = `.map-toolbar` (`.map-zone` name, `.map-z` z-level chips,
  `.map-search` + `.map-count`, `.map-btn` zoom −/+/◎) over `.map-big`
  (pan/pinch/wheel canvas, `touch-action:none`) over `.map-foot` (show-path
  step list / walking progress). **Cross-zone:** the big map can view an
  adjacent zone without moving the player — the toolbar's **`.map-zones`
  "Zones ▾"** button (accent-tinted, beside the zone name) is the signpost:
  it lists every neighbor reachable from an explored border, plus "◎ Back
  to my location" when off-zone (a border room's own menu keeps the same
  "Go to &lt;zone&gt; →" as a shortcut). `.map-zone.offzone` appends a
  "· viewing" cue and ◎ (`.map-btn.active`) becomes "return to my
  location"; pathfinding and autowalk route across zone borders (the
  minimap always stays on the player's zone). `.map-note-pop` is the room-note editor
  (Save/Delete/Close, 2000-char cap); the current room's note renders as
  the `.rose-note` clamped line in the Room panel. `.map-walk` is the
  autowalk cancel chip above the action row — the whole chip cancels
  (44px coarse target). Canvases carry `.menu-opener` so the menus they
  open survive the document's outside-click close. All canvas colors come
  from tokens (`--hud-ter-*` + shared inks) read via `getComputedStyle`.

Verify with `/connect?demo=1` (sample GMCP feeds, no server needed).

---

## Log viewer (staff) — status: shipped (ishar-web#104)

The `/portal/logs/` page (Eternal+). Reuses the console language; adds:

- **`.ac-log` / `.ac-log__line`** — the severity-colored monospace stream,
  rendered inside an `.ac-console__body` (which already scrolls). One line per
  entry; `--error/--warn/--info/--debug/--log` set a left rule + text tint.
  Lines are `textContent`-built from parsed entries (XSS-safe). `.ac-log__note`
  is the amber banner above the stream (e.g. "this color isn't live").
- **`.ac-seg--wrap`** — a **wrapping** segmented control: block-level
  (`display:flex; flex-wrap:wrap`) so it's constrained to its container and
  wraps instead of overflowing. Use for a control with more/longer items than
  fit a phone row (the log viewer's source picker); the plain `.ac-seg` stays
  inline for short 2–3 item controls (deploy console envs).
- **`.ac-subrow`** — an inline `.ac-label` beside its control(s); a lighter row
  than a full `.ac-field`. Hides with `[hidden]`.
- **`.ac-live-dot`** — a small ok-colored dot shown on the blue/green toggle
  label carrying `.ac-seg__item--live`, marking the live color.
- **`.ac-chip__n`** + **`.ac-chip--{danger,warn,info}`** — count suffix and
  semantic tints for the severity filter chips (base `.ac-chip` is neutral).
- Guard: **`.ac-empty[hidden]`, `.ac-filter[hidden]` { display: none; }** — both
  set `display`, so a plain `el.hidden = true` wouldn't hide them (same gotcha
  as `.hud-btn`); the viewer toggles both from JS.

Data comes from the host agent's read-only `log-status` / `log-tail` actions
(see `ishar-mud/docs/infrastructure/deploy_agent.md`); the viewer can't render
end-to-end without that agent, but the markup/CSS eyeball via a `preview.html`
with simulated entries (how this was verified).

---

## When adding a component

1. Check this catalog first — extend, don't fork.
2. Name it `.ac-*`, define it in `admin-console.css`, key it off tokens
   (tokens.md), and guard any motion with `prefers-reduced-motion`.
3. Add it here with markup + status, and log the decision in `decisions.md`.
