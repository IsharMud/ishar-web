# Ishar Web — Claude Code Project Guide

## Project Identity

`ishar-web` is the web presence and staff-tooling layer for **Ishar MUD** — a
text-based MUD with a ~30-year history, maintained by a solo developer. This
repo is **not** the game; the game engine (C + a growing Rust layer) lives in
`isharmud/ishar-mud`. What lives here:

1. **The public site** — home, FAQ, getting-started, MUD-client links, help
   files, leaderboards, challenges, seasons, news/patches, player lookups.
2. **The web telnet client** (`/connect`) — a browser terminal that speaks to
   the live game over a Channels/Daphne websocket bridge (the "HUD").
3. **Staff / admin tooling** — the account portal (`/portal`), feedback triage,
   the **Deploy Console** (`/portal/deploy`, God-gated, drives blue-green
   deploys of the game from a phone), and process/admin views.

The site **shares the game's MariaDB**. Most models are `managed = False` — they
map onto tables the C game engine owns; Django reads and occasionally writes
them but does not own their schema or migrations. Treat the database as a
contract with the game, not something this repo defines.

The active playerbase is small (~10–11 committed mortals) but deeply invested,
and several of them (plus the developer) drive the game from phones. **Mobile
usability is not optional.**

---

## ⭐ The Green-Field Mandate

> **ishar-web is technically brown-field, but the impact zone is small enough
> that we treat it as green field: no concern with breakage or comms — just
> optimal, unhandcuffed design.**

This is the governing constraint. In practice:

- **Don't hedge for backward compatibility** where a cleaner design exists. The
  audience is tiny and known; there is no migration window to protect, no
  external consumers, no deprecation cycle to run. If a page, template, or
  convention is better rebuilt than patched, rebuild it.
- **Reduce entropy, don't preserve it.** The site once carried three
  coexisting visual layers and a lot of copy-pasted markup; the facelift
  roadmap converged them into one console language (complete as of roadmap
  #7). Keep it converged — a reintroduced legacy pattern is a bug.
- **Set conventions, then apply them.** Where a decision improves the whole
  site, make it the standard (record it in `docs/design/decisions.md`) rather
  than scoping it to one page.
- **The one thing you still owe:** correctness and taste. "No concern with
  breakage" means no concern about *changing* things — not a license to ship
  something broken, ugly, or inaccessible. Verify your work (see below).

This mandate **supersedes** any "keeps the existing identity for
compatibility"-style hedging still present in older docs. When you find such a
hedge, treat it as a candidate for a deliberate redesign, not a rule.

---

## Core Development Philosophy

### System Coherence Over Feature Volume

Same north star as the game repo: **every change should reduce entropy.** Before
adding markup, CSS, or a view, ask:

- Does this consolidate or fragment what exists?
- Can it reuse or replace an existing pattern (a component, a mixin, a token)?
- Does it follow the design system (`docs/design/`), or invent a one-off?

### The Solo Developer Constraint

There is no team, no reviewer, no QA. Claude Code is the engineering team this
project doesn't have. Rigor — verification, adversarial thinking about abuse and
edge cases, taste in UX — is the only quality gate. Don't hand-wave "this
probably works"; prove it as far as the environment allows.

### Leave It Better Than You Found It

A corollary of the green-field mandate: **existing code is not precedent.** When
a change routes you through markup, CSS, or a view that predates the current
conventions, converge the part you touch — swap the legacy pattern for its
`.ac-*` / token / mixin equivalent, delete what the change obsoletes — rather
than matching the old style "for consistency." Consistency with debt is just
more debt. Scope it to what you're already touching; a full-page rebuild is its
own task (and often worth proposing).

### Comments

Code should be self-documenting: clear names, small views and functions, obvious
control flow. Comments exist for what the code *cannot* say — and almost nothing
else.

- **Write a comment for**: a non-obvious business rule (the 404-not-403 gating
  convention, `immortal_level` vs. character level), an invariant the code can't
  enforce (a `managed = False` column the game engine owns), or why a surprising
  approach beat the obvious one.
- **Never write a comment that** narrates the next line, restates the function
  name, banners each step of the logic, or describes the *edit* rather than the
  code ("changed X to Y", "new helper for Z"). Commit messages and issues tell
  the story of the change; comments describe only the code as it now stands.
  This applies equally to templates (`{# #}`), CSS, and JS.
- **Terse but intelligent.** One sharp sentence beats a paragraph. If a block
  needs a paragraph to explain, restructure or rename instead of writing prose.
- **Maintain comments like code.** Update or delete stale comments in anything
  you touch — a wrong comment is worse than none.

### Solo-Project Hygiene

- **Commits are the code review record** — small, focused, with messages that
  explain *why*. Six months from now, history is the only reviewer's notes.
- **Delete, don't deprecate** — no external consumers; remove what a change
  obsoletes in the same change.
- **Write decisions down** — a genuine design call goes in
  `docs/design/decisions.md`; a convention worth having is worth applying
  site-wide, not scoping to one page.

---

## Technical Stack

| Layer | Choice |
|---|---|
| Framework | **Django 5.2** (`settings.py`, apps under `apps/`) |
| Server | **Daphne / ASGI** (`asgi.py`), **Channels 4** for the websocket telnet client |
| Database | **MariaDB**, shared with the game. Custom engine `apps.core.backends`; custom PK `apps.core.models.unsigned.UnsignedAutoField`. Most models are `managed = False`. |
| Auth | `AUTH_USER_MODEL = accounts.Account` (a `managed = False` game table) |
| Admin | Django admin, skinned with **django-jazzmin** |
| Frontend | **Bootstrap 5.3.8** + **Bootstrap Icons 1.13.1**, both self-hosted. **No build step.** Small vanilla JS only. Dark-only (`<html data-bs-theme="dark">`, forced). |
| Discord | `discord-py-interactions` bot glue (`discord.py`) |
| Tests | **None.** There is no test suite in this repo today. |

### Frontend rules (non-negotiable)

- **No new frontend libraries.** No CDN dependencies, no web fonts, no
  framework. Ship Bootstrap + Bootstrap Icons (self-hosted) + vanilla JS.
- **Icons via the SVG sprite:**
  `<svg class="bi"><use xlink:href="{% static 'bootstrap-icons/bootstrap-icons.svg' %}#name"></use></svg>`.
- **JS updates the DOM via `textContent` / class swaps, never `innerHTML`** for
  anything derived from data (XSS discipline).
- **Motion is optional:** wrap every transition/animation in
  `@media (prefers-reduced-motion: reduce)`. No motion is load-bearing.
- **Mobile-first.** Every admin tool must be usable at a phone width.

### `static/` is gitignored

`.gitignore` excludes `static/` — it's a collectstatic target
(`docker-entrypoint.sh` runs `collectstatic` on every container start). Source
CSS/JS that must be tracked (e.g. `apps/core/static/css/style.css`,
`admin-console.css`) is **force-added** (`git add -f`). If you add a new tracked
stylesheet or script, remember it won't stage on its own.

---

## Repository Layout

```
apps/                 one Django app per game domain (accounts, feedback,
                      connect, core, leaders, challenges, help, seasons, …)
  core/               shared plumbing: layout.html, mixins, error/home/auth
                      views, custom DB backend, static/css/style.css +
                      admin-console.css, the SVG icon sprite
  accounts/           Account model, portal, deploy console, password, private
  connect/            the web telnet client (Channels consumer + hud.css)
  feedback/           feedback submission + staff triage dashboard
settings.py           single settings module (settings.example.py is the template)
asgi.py / wsgi.py     entrypoints (asgi is the real one — Daphne)
urls.py               root URLconf
docs/design/          ⭐ the living design system — read before any UI work
Dockerfile
docker-entrypoint.sh  collectstatic then exec daphne
```

Shared markup lives in the `ishar` template tag library
(`apps/core/templatetags/ishar.py` — `{% bi %}` icons, `{% crumb %}`
breadcrumbs) plus `apps/core/templates/partials/`, and the `.ac-*` component
layer (`admin-console.css`, loaded globally). Prefer extending the shared
piece over pasting markup — the catalog is `docs/design/components.md`.

---

## Conventions & Patterns

### Views: class-based + mixins

New views are class-based. Staff gating uses the mixins in
`apps/core/views/mixins.py`, which follow a **404-for-everyone-else** convention
(an unauthorized user gets `Http404`, not a 403 — the page simply doesn't exist
for them):

- `GodRequiredMixin` — `account.is_god()` (`immortal_level >= 5`).
- `EternalRequiredMixin` — `account.is_eternal()` (`immortal_level >= 3`;
  equivalent to `is_staff`).
- `NeverCacheMixin` — for sensitive/live pages.

**Immortal levels** live on `accounts.Account.immortal_level`
(`apps/accounts/models/level.py`): None=0, Immortal=1, Artisan=2, Eternal=3,
Forger=4, **God=5**. Do not confuse `immortal_level` with the character *level*
(21+ = immortal) — the gates key off `immortal_level`.

### Action views: POST + JsonResponse

Mutating/admin actions are POST-only CBVs returning `JsonResponse`, CSRF via the
`X-CSRFToken` header (and body field), with an allowlist on inputs. The Deploy
Console (`apps/accounts/views/deploy.py`) and `SetPrivateView`
(`apps/accounts/views/private.py`) are the reference implementations. The
container→host **deploy agent** bridge lives in
`apps/accounts/utils/deploy_agent.py` (a shared unix socket + shared secret;
strict env/service allowlist).

### Surfacing a new staff tool

The canonical place is the **Portal dropdown** in
`apps/core/templates/layout.html` (visible site-wide, grouped by gate), mirrored
by a card on the portal page (`apps/accounts/templates/portal.html`). A tool
that only lives at a hand-typed URL is a bug — wire it into the nav.

---

## The Design System — read this before touching any UI

`docs/design/` is the **living source of truth** for how the site looks and why.
Read [`docs/design/README.md`](docs/design/README.md) first, then:

- [`tokens.md`](docs/design/tokens.md) — the palette: colors, surfaces, text,
  semantics, radii, motion. Every color on a touched page comes from here.
- [`components.md`](docs/design/components.md) — the component catalog
  (canonical markup + status). The **Admin Console** `.ac-*` components
  (`apps/core/static/css/admin-console.css`) are the reference language for
  staff tooling; the Deploy Console is the flagship implementation.
- [`decisions.md`](docs/design/decisions.md) — the append-only ADR log. **When
  you make a genuine design call, record it here** and update the catalog.

Under the green-field mandate the design system is the plan for facelifting the
*whole* site coherently, not just admin pages. If a convention should apply site-
wide, say so in `decisions.md` and start applying it.

---

## Verification (how to prove work without a full run)

The site needs the shared MariaDB **and** the host deploy agent to run
end-to-end; neither is reachable from most Claude Code environments. So verify
as far as you can, and **state plainly what was proven vs. left to the owner's
on-prod test.** Techniques used here:

- **Templates:** compile with Django's template engine via `Template`/
  `from_string()` under stub settings — catches `{% %}`/block errors without a DB.
- **`python manage.py check`** when runnable.
- **`python3 -m py_compile`** on changed Python.
- **Extracted `<script>` blocks:** `node --check`.
- **Visual proof:** build a throwaway self-contained `preview.html` that inlines
  the markup + the CSS layer (and simulates dynamic states), render it with the
  preinstalled headless Chromium
  (`/opt/pw-browsers/chromium*/chrome-linux/chrome --headless=new --screenshot`),
  and send the screenshots. This is how the Deploy Console redesign was
  eyeballed without a live server.
- **Shell:** `sh -n`. **Compose:** `docker compose config`.

Do **not** claim a page works end-to-end when you could only compile it. The
owner tests on production; give them an honest picture of what's verified.

---

## GitHub Issue Tracking

Non-trivial work should be linked to a GitHub issue in the relevant repo
(**`isharmud/ishar-web`** for site work; cross-cutting infra that spans the game
is often tracked in `isharmud/ishar-mud`). Reference the issue number in commits
(`Relates to #NN`) and post a brief completion summary. Trivial changes (typos,
one-line fixes) don't need an issue — use judgment.

When writing an issue, follow the `write-ishar-issue` skill (business impact
first, then technical detail). When writing a PR, follow the `write-ishar-pr`
skill (issue-closing link, Problem/Solution/Verification structure,
screenshots for UI).

**Do not open a pull request unless explicitly asked.** When you do, mirror any
PR template in `.github/` and describe only the diff.

## Deploy

The site is deployed like any game service: **`scripts/deploy.sh prod ishar-web`**
in the `ishar-mud` repo (or the Deploy Console button, which calls the same path
via the host agent). A deploy runs `collectstatic` on container start, so tracked
CSS/JS changes land automatically — but only if they were force-added into git
(see "`static/` is gitignored").
