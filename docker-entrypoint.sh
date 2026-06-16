#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# ishar-web container entrypoint.
#
# Collects static assets on every start so newly-deployed CSS/JS land in the
# /app/static volume that nginx serves — no more "forgot to run collectstatic"
# after a deploy. Then hands off to the CMD (daphne).
#
# collectstatic needs no database and is idempotent (it skips unchanged files).
# If it fails — e.g. the bind-mounted static dir isn't writable on a fresh box —
# we warn and still start the server, so a static-perms hiccup degrades to stale
# assets rather than a dead site.
# ─────────────────────────────────────────────────────────────────────────────
set -e

python manage.py collectstatic --no-input \
    || echo "WARN: collectstatic failed — static assets may be stale (check /app/static perms)" >&2

exec "$@"
