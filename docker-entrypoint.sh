#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# ishar-web container entrypoint.
#
# Applies pending DB migrations and collects static assets on every start, so a
# deploy carries both the schema and the assets a new build needs — no more
# "forgot to run migrate/collectstatic" after a deploy. Then hands off to the
# CMD (daphne).
#
# migrate only touches the Django-managed tables this repo owns (clients, faqs,
# feedback, news, patches, notes, core bookkeeping, django_* ). The game's own
# tables are mapped by managed=False models and produce no migrations, so they
# are never altered here. Applying committed migrations is what keeps the site's
# schema in step with its models — without it, a new column (e.g. the featured
# MUD-client fields) turns every page that reads that table into a 500.
#
# Both steps degrade rather than kill the container: a migrate that can't run
# (DB unreachable, or the app user lacks ALTER) or a collectstatic that can't
# write leaves the previous schema/assets in place and still starts the server,
# so a transient hiccup is a warning, not a dead site.
# ─────────────────────────────────────────────────────────────────────────────
set -e

python manage.py migrate --no-input \
    || echo "WARN: migrate failed — database schema may be behind (pending migrations not applied)" >&2

python manage.py collectstatic --no-input \
    || echo "WARN: collectstatic failed — static assets may be stale (check /app/static perms)" >&2

exec "$@"
