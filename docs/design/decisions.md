# Design Decisions Log

An append-only record of design decisions, newest first. Lightweight ADR: what
we decided, and why. When you make a real design call — a new component, a token
change, a deliberate deviation — add an entry. Don't relitigate settled ones;
supersede with a new dated entry if something genuinely changes.

Format: `## YYYY-MM-DD — Title` · **Decision** · **Why** · (optional) **Notes**.

---

## 2026-07-15 — Web client: NUL-sentinel control channel and liveness policy

**Decision.** Issue #74. Websocket text frames starting with NUL (`\x00`) are
formally the telnet bridge's out-of-band **control channel**: server→client
`\x00ECHO_ON/OFF`, `\x00GMCP <msg>`, `\x00PONG`; client→server `\x00PING`.
The consumer answers PING with PONG only while its telnet leg is healthy (a
dead bridge answers with a 4502 close), and **never forwards a NUL-prefixed
frame into the game**. Client liveness policy: a 45 s visible-tab probe
interval plus probe-or-force-reconnect on wake events (tab visible, `online`,
bfcache `pageshow`); going offline **parks** reconnection until the network
returns instead of burning the backoff ladder; a clean close (code 1000, the
game ended the session) is never auto-revived. The consumer also introduces
itself to the game on GMCP negotiation (`Core.Hello` "IsharWeb" +
`Core.Supports.Set` naming the packages the HUD consumes).

**Why.** Phones switch networks and freeze tabs; a half-open socket looks
OPEN and goes nowhere, and the #85 reconnect ladder only fires when the
browser *knows* the socket closed. The probe closes that gap; the offline
park keeps the ladder meaningful; the never-forward rule closes a latent
injection hole where crafted control frames could reach the telnet stream.

## 2026-07-15 — Web client: session continuity lives in web storage; xterm addons are within the xterm decision

**Decision.** Issue #74. Continuity storage is split by scope: **localStorage**
for device-level state — `ishar.history` (command history, last 200),
`ishar.aliases`, `ishar.settings` (gear-menu toggles) — joining the existing
`ishar.fontsize/hud/tab/colL/colR`; **sessionStorage** for per-tab session
state — `ishar.term`, the terminal scrollback re-encoded to clean ANSI
(last 1500 lines, ≤512 KB, front-truncated at a line break) on
pagehide/tab-hidden and replayed with a dim divider on the next load.
Reconnects (manual included) no longer clear the terminal, and the HUD's
`reset()` keeps the chat log — chat is history, not game state. Chat does
*not* persist across page loads. Vendoring `@xterm/addon-serialize` and
`@xterm/addon-search` (0.13.0/0.15.0, the pairs for the vendored xterm
5.5.0) is ruled **within the existing xterm decision**, not new frontend
libraries: same package family, same self-hosted minified-UMD form as the
fit/web-links addons, feature-checked so a missing file degrades cleanly.

**Why.** The one thing a player wants after a drop or a fat-fingered reload
is what just happened. sessionStorage is deliberately per-tab (no multi-tab
clobber, no stale week-old logs); passwords never enter history (the
pipeline bypasses password mode — also fixed retroactively).

## 2026-07-15 — Web client: the `/` client-command namespace; stacking on by default with a comm guard

**Decision.** Issue #74. Input lines starting with `/` are handled in the
browser (`/alias`, `/unalias`, `/stack`, `/settings`, `/clear`, `/help`;
`//text` escapes a literal `/`). Aliases expand once (no recursion), support
`$1`–`$9`/`$*`, and pass a safeCmd-style guard. **`;` command stacking is on
by default** (owner's call) with the hazard managed two ways: a line whose
first token (2+ chars) prefix-matches a comm verb (say/tell/gossip/…) or
starts with the say-quote `'` never splits — so `say hi; how are you` stays
one command while `e;n;w` walks (single letters stay splittable: `e` is
east, not emote) — and `;;` sends a literal `;`. Password entry (server
ECHO suppressed) bypasses the entire pipeline. Touch history is a popover
(`#history-pop`) anchored to the input, not the HUD sheet: it must work with
the HUD off, and the sheet is mobile-only and re-parents panels.

**Why.** These are the ergonomics every desktop MUD client ships; doing them
client-side keeps the game's parser untouched. The comm guard + `;;` escape
kill the classic "split my sentence" misfire without hiding the feature
behind a setting nobody finds.

## 2026-07-15 — HUD hot paths are DOM-built; cold panels keep esc()+innerHTML

**Decision.** Issue #74. The HUD's rendering splits by frequency. **Hot
paths** — chat (per message), the hotbar cooldown tick (per second), the
vitals bars (every game pulse) — build/update real DOM nodes
(`createElement`/`textContent`, cached refs, in-place width/text updates,
identical-payload skip for `Char.Vitals`). **Cold panels** — room, equipment,
inventory, train, status, who, re-rendered at human-action frequency — keep
their `esc()`+innerHTML templates as a documented, scoped exception to the
site-wide "textContent, never innerHTML" rule. Hotbar buttons always carry
both the countdown and percent spans; a `.cooling` class picks which shows.

**Why.** Rebuilding 200 chat lines per message and every hotbar button every
second is real waste on a phone on battery; rewriting six cold panels to DOM
building buys nothing measurable and doubles the markup surface. The esc()
discipline in the cold templates is centralized and audited — the exception
is a boundary, not an erosion.

## 2026-07-13 — `/skills` shows only what a mortal may see (visibility gate)

**Decision.** The public skill pages replicate the game's mortal-visibility
predicate (ishar-mud `info.c` `stack_skills_by_type` mort_only path), not a raw
read of `class_skills`. A skill is shown only if **(1)** its `skill_type` is
Skill / Spell / Passive — Craft, Enchant, and the internal Type marker are
excluded (`skill_types_t` enum: TYPE=0, SKILL=1, SPELL=2, CRAFT=3, ENCHANT=4,
PASSIVE=5 → show 1/2/5); **(2)** some **playable** class can learn it
(`class_skills.min_level >= 0 AND max_learn > 0`) or some **playable** race can
(`races_skills.level >= 0`) — mirroring `can_class/race_learn_skill >= 0`; and
**(3)** it isn't gated to a not-yet-live season (`seasons.new_features_on` off
→ the 13 gated `enum_symbol`s are hidden). One predicate,
`apps/skills/utils.visible_skills()`, gates the index, the detail page,
`find_skill_by_name` (so the `help <skill>` fallback and direct URLs 404 for
hidden skills), and every "did you mean" suggestion. Class/race associations on
a detail page are likewise filtered to playable + learnable, mirroring
`display_skill_full`'s mortal loops.

**Why.** A public, crawlable page must not surface deprecated enchants,
immortal / mob-only skills, or unreleased-season content the game deliberately
hides from mortals (they were cluttering the Mage/Necromancer lists). Reading
raw join rows exposed all of it; the centralized predicate is the single source
of truth so the four entry points can't drift.

## 2026-07-13 — DB-driven skill/spell pages (`/skills`) and the help→skill merge

**Decision.** The dormant `apps/skills` app is now a public surface: `/skills/`
(a searchable index grouped by class, plus a "Racial" bucket) and
`/skills/<name>/` (one skill/spell), built entirely on existing `.ac-*`
components — `.ac-hero`, `.ac-panel`, `.ac-tablewrap`/`.ac-table` for the
"Learnable By" class/race levels, `.ac-kv` for details, `.ac-filter`/`.ac-chip`
for forces + the class jump-nav, `.ac-quote` for the description, `.ac-empty` +
a did-you-mean chip row for 404s. No new CSS. Wired into the Help nav dropdown.
The detail page mirrors the in-game `skill` command (`display_skill_full`),
minus per-player state: type, classes/races with learn levels, stat pairing,
quick/standard action, position, save, cooldown, category, forces, description.

Help and skills are **merged** the way the game's `help` does
(`ishar-mud src/dbase/help.c`): a help lookup with no helptab topic falls back
to a skill-name match and redirects to `/skills/<name>/`, and deprecated
`Spell *`-prefixed helptab topics redirect to their live skill page instead of
rendering stale text. **Why.** The game retired per-skill helpfiles for the
dynamic `skill` command; the website only ever parsed `helptab`, so skill-only
topics (Earthquake, Meteor Swarm — issue #51) were simply missing. Reading the
shared DB the game already owns closes that gap with no bridge, and routing
deprecated spell topics to the live data reduces entropy (one source of truth).

**Notes.** Flag-derived fields (quick/standard action, movement) read
`spell_flags` names heuristically and should be spot-checked on prod. Managed
= False models; two harmless read-only field additions (`Force.display_name`,
skill display helpers).

## 2026-07-13 — Deterministic help search ladder (name before alias)

**Decision.** `HelpTab.search` sorts each topic into the single strongest tier
it matches and returns the first non-empty tier: **exact name → exact alias →
name prefix → name substring → alias prefix → alias substring** (all
case-insensitive), name matches ranked above alias matches. This supersedes the
old single substring sweep over every name and alias. **Why.** The old sweep
had no relevance order and over-matched: searching "heal" returned "Score"
because its "Health" alias *contains* (and even prefixes) "heal". Ranking
name-substring above alias-prefix returns the actual `Spell Heal*` topics and
drops Score entirely — verified against the live 563 KB helptab. The ladder
also gives 404s "did you mean" suggestions (stdlib `difflib`) drawn from both
topic names and skill names. Deliberately one tier finer than the original
5-tier sketch, because real data showed a 5-tier ladder still surfaced Score.

## 2026-07-12 — Featured clients (`.ac-link--featured`) and a browser-first clients page

**Decision.** `/clients` now leads with an **In Your Browser** panel — hint
copy naming the HUD's capabilities plus the amber `.ac-cta--accent` "Play in
your browser" — before any downloadable client, and the client grid gains a
**featured** treatment: `.ac-link--featured` (amber-washed card, amber name)
with a `star-fill` icon tile, an accent "Ishar package" pill, and a note
line. Featured status is **data-driven**: `MUDClient.is_featured` +
`MUDClient.featured_note` (migration `clients.0008`, which also flags
**Mudlet** with "install the Ishar package from Mudlet's package
repository" and sorts featured clients first in their category). Both fields
are editable in the admin.

**Why.** The web client is now a first-class way to play (roadmap #6b) and
deserves top billing on the "how to connect" page, and Mudlet ships an
official Ishar package — that's a real support difference the grid of
otherwise-equal cards was hiding. Keeping the flag on the model (not
hardcoding "Mudlet" in the template) means the next specially-supported
client is an admin edit, not a deploy.

## 2026-07-12 — Roadmap #7: the whole public site speaks the console language; the classic layer is retired

**Decision.** The last mile of the facelift. Every remaining public template —
home, error, help (topic + index), world, upgrades, FAQ, get-started, clients,
support, history, events, news, patches (+ latest), who, player profile,
search results, season, login, password, flatpages — is rebuilt on the shared
components: `{% crumb %}` breadcrumbs, `.ac` containers, `.ac-hero` page
headers, `.ac-panel` prose sections, `.ac-rows` record lists (events, patches,
who, upgrades, results), `.ac-quote` for captured game text (help bodies, the
get-started excerpts), `.ac-kv` details, `.ac-note` callouts, `.ac-empty`
empty states, and a shared `.ac-pager` treatment for news/patches paging.
Along the way:

- **The classic layer is gone.** The black `.card`/`.list-group` overrides,
  `.btn-ishar`, `.past-news`, `.nested-list`, and `.remort-upgrade-row` CSS
  are deleted; no template renders Bootstrap cards, list-groups, contextual
  badges, page-link pagination, or dismissible info alerts anymore. Bare
  (classless) form elements now default to console-field styling so
  Django-rendered forms (password change) look native.
- **Dismissible alerts are retired on info pages** — static page copy is not
  a notification; it renders as hero subs, panel prose, or `.ac-note`s.
- **jQuery + DataTables are deleted** (`static/datatables/`,
  `jquery-3.7.1.min.js`) now that `upgrades.html` renders as filterable
  `.ac-rows` (same vanilla-JS filter pattern as leaders).
- **`--ac-immortal` (`#00b7eb`)** joins the token set with an
  `.ac-pill--immortal` variant (player profile); the `.god-player` family
  references it.
- **Component hardening:** anchor CTAs/buttons pin their colors against the
  global `a:link` rule (`a.ac-cta`, `a.ac-btn--*`); `.ac-row__side` wraps its
  pills instead of clipping on phones; `.two-col` gets a column gap.
- **Home is rebuilt as a real front door:** latest news hero + body, the
  pitch, and a Play Now panel with an amber browser-client CTA and host/port
  details (also fixes the long-standing unbalanced `</div>` in the old
  template). The popover on the player profile is replaced with panel-hint
  prose, per the portal decision.

**Why.** This was the point of the green-field mandate: one visual system,
not three. Public pages were the last holdouts of copy-pasted breadcrumbs,
black-outline boxes, and a ~1MB framework tax for one sortable table. The
site now draws every surface from one token + component layer, so a palette
or component change reaches everything.

**Notes.** Verified with the stub-settings render harness (32 page/context
combinations), `node --check` on inline scripts, and headless-Chromium
screenshots at 1280 px and 390 px with `scrollWidth == innerWidth` asserted on
every page (mobile checklist #1). Left to on-prod eyes: real data volumes
(long help bodies, huge topic lists) and the PDF `<object>` embed on phones.

## 2026-07-12 — admin-console.css loads globally

**Decision.** `layout.html` now loads `admin-console.css` on every page,
right after `style.css`; the per-page `{% block includes %}` links are gone.
This supersedes the "load per page via `{% block includes %}`" convention in
the component catalog.

**Why.** With roadmap #7 the console components are the site's language, not
a staff-tooling dialect — every page uses them. One content-hashed, cached
stylesheet is cheaper than per-page include boilerplate, and it removes a
whole class of "forgot the include" bugs on new pages.

## 2026-07-12 — The connect session is a first-class surface: terminal-first phones, collapsible desktop columns

**Decision.** Roadmap #6b. `/connect` is rebuilt as a fully supported product
surface on both form factors, and the HUD is **on by default** (persisted
opt-out via the toggle).

*Phones are terminal-first.* The old stacked layout (topbar pile → tabs →
terminal → panels, game below the fold) is gone. The grid is topbar /
terminal / dock: panels live behind a thumb-reach **bottom dock** (Room, Gear,
Bag, Char, Status, Chat, Who) and open one at a time as a **bottom sheet**
over the terminal — acting from the sheet (an exit tap, a tell prefill)
dismisses it, as does tapping outside; Chat gets an amber unread dot. Panel
sections are single DOM nodes re-parented between their desktop columns and
the sheet on the 768px flip, so the render layer is unchanged. The topbar
collapses to status dot + name + wrapping vitals row; the world line and
gold/TNL group hide (Status carries gold/TNL/bank there). The hotbar is one
horizontally scrollable row; the send button is a 44px icon; all HUD controls
get coarse-pointer sizes and `:focus-visible` rings.

*Desktop is a session dashboard.* Side columns collapse **individually**
(topbar toggles, persisted; pressed = open) so mid-width screens keep a
full-width terminal — below 1200px the left column starts collapsed, and
both-closed is a deliberate "zen" mode. The terminal always takes the
leftover space. **Terminal font size** is user-adjustable (A−/A+, 10–22px,
persisted).

*The shell recedes on this page* (`body.connect-page` via a new layout
`body_class` block): 2.4rem logo, no breadcrumb line, tight content frame,
no footer. The session owns the viewport.

**Why.** The playerbase drives the game from phones and the old HUD was
desktop-first scaffolding — fixed columns that squeezed the terminal below 80
columns on laptops, and a phone layout that buried the game under ~500px of
chrome with 5px tap targets. A MUD client's one non-negotiable is that the
terminal is primary; every mode above (dock/sheet, collapsible columns, zen)
is that principle applied. Defaulting the HUD on makes the flagship
experience the default one now that Season 15's GMCP feeds are live.

**Notes.** Verified with the demo-mode harness (headless Chromium +
Playwright): 1440/1024/390px screenshots across HUD-on/off, sheet open,
columns collapsed; `scrollWidth == viewport` asserted at every size. The
telnet/GMCP bridge internals are deliberately untouched (tracked separately).

## 2026-07-12 — The connect HUD runs on the shared tokens; `--hud-*` shrinks to HUD-domain meanings

**Decision.** Roadmap #6. `hud.css` no longer defines its own copies of the
structural palette — surfaces, borders, text, dim, and accent reference
`--ac-*` directly (the duplicate `--hud-bg/panel/border/text/dim/accent`
aliases are deleted, along with every ad-hoc grey: `#1c1c22`→`--ac-elev`,
`#17171c`→`--ac-elev`, `#000` wells→`--ac-bg`, `#222`→`--ac-border`). The
`--hud-*` set now covers only HUD-domain meanings: the vitals triple aliases
the shared semantics (`--hud-hp: var(--ac-danger)`, `--hud-mp: var(--ac-info)`,
`--hud-mv: var(--ac-ok)` — one red site-wide; the old `#cc3333` hp is gone) and
the flavor colors with no site-wide equivalent get named tokens
(`--hud-gold/-gold-wash/-tgt/-mm/-edge/-event/-moon`). Along the way the HUD
joins the shared conventions: radii from the token scale (`--ac-radius-sm`
panels/tabs/buttons/skills, `--ac-radius` banner, `999px` season pill),
`.hud-btn` aligned with `.ac-btn` (elev surface, `--ac-border-2`, amber
hover, `:focus-visible` outline), amber-tinted borders as `rgba(255,170,119,…)`
per the console idiom, the season-15 banner on `--ac-wash` over `--ac-panel`
instead of hardcoded browns, and the previously missing
`prefers-reduced-motion` guard. Affect/skill category edges use the semantic
tokens (ok/danger/info). Two deliberate true-blacks remain: the terminal
canvas (matches the xterm theme) and the bar-text shadow.

**Why.** The HUD predates E1 and carried a parallel token set with identical
values — pure entropy once the shared base existed. Re-expressing it makes a
palette change a one-line edit that reaches all three visual layers, and the
remaining `--hud-*` names now say something true: "this color means a
HUD-domain thing," not "this is the HUD's copy of the same grey."

## 2026-07-12 — Leaders & Challenges adopt the console language; DataTables retired page-by-page

**Decision.** Roadmap #5. **Leaders** keeps a real table — it is genuinely
column-comparable data — via the new `.ac-tablewrap` / `.ac-table` component:
token-aligned, horizontally scrollable inside its own container (the page
never overflows), uppercase dim sortable headers as real `<button>`s with
state on `th[aria-sort]`, tabular-nums numeric columns, an amber podium for
the top three ranks, and the player's class as a sub-line under the name.
Sorting and the name/class filter are ~40 lines of vanilla JS. There is **no
game-type filter UI**: only one mode is live at a time (Classic in normal
seasons, Hardcore in Fated), so chips for All/Classic/Hardcore/Survival were
pure clutter — the per-type URLs (`/leaders/classic/`, …) stay routable for
whenever that changes. **Challenges**
drops its table entirely: eight-ish weekly kill targets are a checklist, not
a matrix, so they render as `.ac-rows` — constraint meta (party size, level
cap) with icons, an ok "slain" pill + winners when complete, and the new
`.ac-row--done` modifier (ok-green strike-through — done, not dead; the old
red `.challenge-completed` is deleted). Completion tiles double as the
All / Still Standing / Slain filters over the existing URLs, and the
next-cycle time is a live hero pill. **jQuery + DataTables are gone from
both pages**; the vendored assets stay only until `upgrades.html` (roadmap
#7) migrates, then get deleted. `.ac-row:target` (amber wash) is the deep-link
highlight for row anchors.

**Why.** DataTables + jQuery was ~1MB of framework to sort ten players and
search eight mobs, and its chrome (page-length menus, column-visibility,
search builders) never matched either the design language or the data size.
The row treatment tells the truth about challenges — a weekly hit-list players
check off — while `.ac-table` gives the site one honest, token-aligned table
for data that really is tabular. These are also the first *public* surfaces
on the console language, per the green-field mandate.

## 2026-07-12 — Static assets are content-hashed (cache busting)

**Decision.** `{% static %}` URLs carry a content hash
(`style.2aed1762….css`) via `ManifestStaticFilesStorage` — subclassed in
`apps/core/storage.py` as non-strict, with dangling third-party references
(jazzmin's unshipped sourcemaps) left unhashed instead of failing
collectstatic. Consequences for design work: **never rely on a same-name CSS
edit reaching users** (that's now guaranteed by the hash), templates must
reference assets through `{% static %}` (or `{% bi %}`), and load-bearing
presentation must not live only in a stylesheet a stale cache could hold —
the shell's logo keeps a `height` attribute fallback for exactly that reason.

**Why.** Round 2 shipped new templates whose logo sizing lived only in
`style.css`; phones holding the cached old sheet rendered a full-size logo
(and blue oversized breadcrumbs) — new markup styled by old CSS. With hashed
filenames a stylesheet change changes its URL, so templates and styles always
arrive as a matched set.

## 2026-07-12 — Mobile friendliness is a gating requirement (with a checklist)

**Decision.** Every shipped surface must pass this checklist at a true 390px
viewport before it lands — it is a release gate, not an aspiration:

1. **No horizontal overflow** — `document.scrollWidth == viewport width`.
2. **Form fields ≥ 16px** (`1rem`) — sub-16px inputs make iOS Safari zoom-jump
   on focus, the single most jarring mobile failure.
3. **Comfortable tap targets on touch** — `@media (pointer: coarse)` bumps
   `.ac-btn` / `.ac-chip` / `.ac-copy` padding; new interactive components must
   join that block.
4. **No hover-only affordances, no sticky lifts** — anything conveyed on hover
   must also be visible statically, and hover `transform`s are suppressed under
   `@media (hover: none)` so a tap doesn't leave a component stuck mid-"lift"
   (`.icon-link-hover` included).
5. **Shell rows stack, never squeeze** — multi-column rows (footer, season bar)
   use `col-12 col-sm`-style stacking at phone width; columns must never
   compress until words wrap letter-by-letter.
6. **Compact chrome at `<576px`** — heroes, panels, and the logo shrink;
   vertical space on a phone is content space.
7. **Verification includes phone proof** — full-page screenshots at 390px plus
   the scrollWidth assertion (the headless-Chromium/Playwright harness), and
   when the owner reports feel-jank on a real device, that report wins over a
   passing screenshot.

**Why.** The playerbase and the developer drive the game from phones; this has
always been principle #7, but round 2 of the facelift still shipped
desktop-first regressions (iOS focus zoom, squeezed footer columns, sticky
hover transforms). A vibe is not a gate; a checklist is. This entry supersedes
"mobile-first" as prose — cite the numbered items in review.

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

## 2026-07-13 — Data visualization: single-hue server-rendered bars

**Decision.** Charts on staff surfaces are server-rendered `.ac-bars` —
single-series horizontal magnitude bars, one hue per group (`--ac-info`
default, amber only as a deliberate second group), widths computed
server-side, values as text-token labels at the tip, always accompanied by
the exact numbers (inline or a paired `.ac-table`). No charting library, no
canvas, no client-side rendering. **Why.** The site's no-new-frontend-library
rule already forbids chart libs; single-hue bars with direct labels are the
one chart form that stays honest at this data scale (~10 players, ~14
seasons), works at phone width, needs no legend, and degrades to nothing —
the numbers are always present as text. Color encodes nothing per-row
(identity is the label), so colorblindness cannot cost information.

## 2026-07-15 — Log viewer: severity-tinted stream + wrapping segmented control

**Decision.** The staff log viewer (`/portal/logs/`, Eternal+) renders logs as a
severity-colored monospace stream (`.ac-log` / `.ac-log__line--{error,warn,info,
debug,log}`) inside an `.ac-console__body`, driven by a server-side parser that
classifies each line's level/tag/timestamp. Level is set only from an **explicit
token** (`ERROR`, `[WARN]`, `BUG:`, `SYSERR:` …), never guessed from prose;
indented lines are treated as continuations of the entry above. The blue-green
**live color is highlighted** (a `.ac-live-dot` on the toggle + a `LIVE: <color>`
hero pill) while **both colors stay viewable**. Added two reusable pieces:
`.ac-seg--wrap` (a block-level, wrapping segmented control — the base `.ac-seg`
is `inline-flex` and sizes to content, so a 3+ item control overflows a phone;
the wrap variant is width-constrained and wraps) and `.ac-subrow` (an inline
label + control row). **Why.** Severity tint + parsed facets make a 5000-line
tail scannable on a phone; token-only level classification avoids false-positive
coloring; the wrapping seg fixes an overflow the 2-item deploy console never hit.
Also guarded `.ac-empty[hidden]` / `.ac-filter[hidden]` — both set `display`,
which defeats a plain `el.hidden = true` (same gotcha already noted for
`.hud-btn`), and the viewer toggles them from JS.

**Architecture note (cross-repo).** The web container can't see the per-color log
volumes, run docker, or read the proxy's live color, so the viewer reads through
**read-only** `log-status` / `log-tail` actions added to the host agent
(`ishar-mud` `scripts/deploy-agent.py`) — the same allowlisted, argv-exec'd
boundary as the deploy button (see `ishar-mud/docs/infrastructure/deploy_agent.md`).

## 2026-07-15 — Patch Notes web surface (distinct from front-page News)

**Decision.** The game's in-game `news` command (the `patch_notes` system) gets a
web face — a public viewer (`/patch-notes/`) and an Eternal+ editor/publisher
(`/patch-notes/console/`) — built in a new `apps/patchnotes` app in the console
`.ac-*` language. It is kept **separate** from the existing front-page **News**
(`apps/news`), which stays as-is: front-page announcements are a different use
case (a News redesign is deferred). To avoid two things called "News," the game
system is labeled **"Patch Notes"** everywhere on the web (its real identity).
**Why.** Green-field entropy control cuts both ways — these are genuinely two
concepts (site announcements vs. game patch notes with per-account read state),
so we name them apart rather than force a merge.

**Bridge.** Reads and per-account read state (`account_patch_notes_read`) are
direct on the shared DB. Publishing writes `patch_notes` state directly (note is
live on the site instantly) and enqueues one `patch_notes_sync_queue` row the
game drains to post the Discord announcement — the web container holds no
webhooks. This mirrors the feedback side-effect-replay outbox; contract in
`ishar-mud/docs/patch_notes_web_contract.md`.

**Body rendering.** Note bodies use the game's markdown subset (`## head`,
`- bullet`, `**bold**`). Server-side `apps/patchnotes/markdown.py` escapes then
emits that subset (safer than the News page's `autoescape off`); the editor's
live preview builds the same DOM client-side with `textContent` only — no
`innerHTML`, honoring the XSS rule above.

---

## Open decisions / to record when made

- ~~**Live styleguide page**~~ — built (`/styleguide`, Eternal+; see entry above).
- ~~**Public-shell facelift**~~ — resolved by roadmap #4–#7: the console
  surfaces are the whole site's language now; the amber-border look survives
  only as brand accents (navbar edge, hero edges), not as panel chrome.
