---
name: write-ishar-issue
description: Standard structure for GitHub issues for Ishar site work — business impact first, then technical detail. Use every time an issue is created or substantially rewritten in isharmud/ishar-web (or ishar-mud for cross-cutting work).
---

# Writing an Ishar Issue

Issues are this project's memory and its only planning artifact. Write each one
so that future-you, reading cold in six months, can judge whether it still
matters and how to start. That means impact before implementation, always.

## Where to file

Site work goes to `isharmud/ishar-web`. Cross-cutting infrastructure that
spans the game (deploys, shared DB contract) is usually tracked in
`isharmud/ishar-mud`.

## Before filing

- **Search for duplicates** (`search_issues`) before creating. If a near-match
  exists, comment there instead of filing new.
- **One issue per unit of work.** If the description needs the word "also,"
  it's probably two issues.

## Title

Terse, specific, searchable. Name the surface and the behavior, not the
implementation:

- ✅ `Deploy Console: status poll stops after network blip`
- ✅ `Leaderboards unreadable at phone width`
- ❌ `Fix JS bug`
- ❌ `Portal improvements`

## Body structure

### 1. Lead with business impact (no heading — it's the opening)

The first paragraph answers *why this matters* before any code is mentioned:
who hits it (players, staff, the developer deploying from a phone), what it
costs (usability, trust, security exposure, deploy safety), or what debt it
retires. The audience is ~11 players plus staff who drive everything from
phones — "who hits this and what happens to them" is almost always
answerable. If you can't articulate an impact, question whether the issue
should exist.

> The Deploy Console's status poll silently dies after a dropped request, so
> a deploy started from a phone on cell signal shows "in progress" forever.
> The one person who deploys does it from a phone; this makes the flagship
> staff tool untrustworthy exactly when it's needed.

### 2. `### Technical details`

What's actually going on: affected apps/templates/views, root cause if known,
relevant constraints (shared game DB is a contract, `managed = False` models,
no test suite, mobile-first). Short is fine — "root cause unknown; start in
`deploy.js` poll loop" beats padding.

### 3. `### Acceptance criteria` — for multi-part work

Checkboxes that define "done." For UI work, include the mobile check
explicitly ("usable at 390px width") — it is not optional here.

### For bugs, also include

- **Reproduction steps** — URL, account gate level, and sequence; or "not
  reproduced; observed via <report/log>."
- **Observed vs. expected** behavior, one line each.

## Labels

Use the repo's existing labels; don't invent new ones without asking.

## Anti-patterns

- Opening with a traceback or template path — impact first, always.
- Solution-shaped issues ("Add a retry flag") that never state the problem.
- Padding. Terse and complete beats long and thorough-looking.
