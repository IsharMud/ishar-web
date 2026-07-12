"""
Static-files storage with content-hashed filenames (cache busting).

Browsers cache stylesheets hard, so a shipped CSS change may otherwise render
new templates with a stale sheet (e.g. the round-2 shell with the old logo
sizing). ManifestStaticFilesStorage makes every {% static %} URL change when
the file's content changes, so caches can never go stale.

Non-strict: an asset missing from the manifest falls back to its plain name
instead of raising — consistent with docker-entrypoint.sh, where a failed
collectstatic degrades to stale assets rather than a dead site.
"""
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class IsharManifestStaticFilesStorage(ManifestStaticFilesStorage):
    manifest_strict = False

    def hashed_name(self, name, content=None, filename=None):
        # Third-party assets (e.g. jazzmin's vendored bootstrap) reference
        # sourcemaps that were never shipped; leave such dangling references
        # unhashed instead of failing the whole collectstatic run.
        try:
            return super().hashed_name(name, content, filename)
        except ValueError:
            return name
