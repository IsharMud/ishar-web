---
name: write-ishar-pr
description: Standard structure for pull requests in isharmud/ishar-web — issue-closing link, Problem/Solution/Verification sections, screenshots for UI. Use whenever opening a PR or drafting a PR description (only open PRs when explicitly asked).
---

# Writing an Ishar PR

A PR body has two jobs: let future-you understand the change without reading
the diff, and teach whatever the change required learning. The diff shows
*what* changed — the body explains *why* and *how it works*. Never narrate
the diff.

## Title

Imperative mood, like a commit subject: `Recover Deploy Console status poll
after failed request`. Name the behavior change, not the files touched.

## Body structure

### 1. Issue link — first line, always

```
Closes #NN
```

Use a closing keyword (`Closes`/`Fixes`/`Resolves`) so the issue closes
automatically on merge — a plain `#NN` mention does not close anything.
If the issue lives in the game repo, the cross-repo form works too:
`Closes IsharMud/ishar-mud#NN`. If no issue exists for non-trivial work,
create one first (see `write-ishar-issue`).

### 2. `### Problem`

The problem being solved, self-contained — a reader should not need to open
the linked issue. Lead with the impact (same rule as issues), then the
technical shape of the problem. Two to five sentences is usually right.

### 3. `### Solution`

What was implemented and *why this shape*. Aim to teach: surface the one
non-obvious decision, mechanism, or tradeoff a future reader would need —
the thing you'd forget in six months. Stay terse and approachable: short
paragraphs, plain language, no jargon walls. If an alternative was seriously
considered and rejected, say so in one line. Record genuine design-system
calls in `docs/design/decisions.md`, not only in the PR.

### 4. `### Verification`

This repo has no test suite, so this section replaces "Test coverage" and is
**required for any behavior change**. State plainly what was proven and how
(template compile, `manage.py check`, `py_compile`, `node --check`, headless
Chromium screenshots) versus what is left to the owner's on-prod test.
Honesty over optics — "compiled but not run against the live DB" is a valid
entry; a claim of end-to-end verification that didn't happen is not.

**UI changes require screenshots**, including one at phone width. Build the
throwaway `preview.html` + headless Chromium proof described in CLAUDE.md.

### 5. Situational sections

- `### Deploy notes` — required if the change touches settings, the deploy
  agent, static assets (was the new file force-added? `static/` is
  gitignored), or anything the game DB contract depends on.

## Scope

One PR per issue. If the branch accumulated unrelated fixes, note them
explicitly in the body — or better, split them out.

## Anti-patterns

- A body that lists changed files (the diff already does).
- `Closes` pointing at an issue the PR only partially resolves — use
  `Relates to #NN` and say what remains.
- Screenshots of desktop only for a UI change.
- Teaching by volume. One well-explained decision beats ten paragraphs of
  walkthrough.
