"""Tolerant log parsing for the staff log viewer (ishar-web#104).

Turns a raw log tail (from the host agent) into structured entries so the page
can offer level/tag filter chips, a search box, and a timeframe readout. The
three sources have three shapes and none is guaranteed:

- **runlog** — the C game log: ``YYYY/MM/DD HH:MM:SS <message>[: errstr]``. Most
  lines carry no level; a few use game conventions (``BUG:``, ``SYSERR:``).
- **stderr** — Rust ``env_logger`` (``[2026-07-15T..Z INFO] msg``) + ``eprintln!``
  (often ``Rust: ...``) + C panics/perror. Bracketed level is common.
- **web** — Daphne/Django: a grab-bag (access lines, ``LEVEL msg``, tracebacks).

So the parser never *requires* a shape. It extracts a leading timestamp when one
of a few known formats is present, classifies a level from an explicit token
only (never guessed from prose, to avoid false positives), and pulls a leading
``LABEL:`` / ``[label]`` tag when present. Anything unrecognized is a plain
``log`` entry; a line with no timestamp (a stack-trace continuation) inherits the
previous entry's timestamp so it groups sensibly in the timeframe.
"""
import re

# Normalized levels, most severe first — also the CSS severity classes (.ac-log--*).
LEVELS = ("error", "warn", "info", "debug", "log")

# Explicit level tokens → normalized level. Matched only as whole words near the
# start of a line, so ordinary prose containing "info" doesn't get miscolored.
_LEVEL_TOKENS = {
    "error": "error", "err": "error", "crit": "error", "critical": "error",
    "fatal": "error", "panic": "error", "syserr": "error", "emerg": "error",
    "alert": "error",
    "warn": "warn", "warning": "warn", "bug": "warn",
    "info": "info", "notice": "info",
    "debug": "debug", "trace": "debug",
}

# Leading timestamp formats, tried in order. Each capture group 1 is the stamp.
_TS_PATTERNS = (
    re.compile(r"^(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})\b"),          # runlog
    re.compile(r"^\[?(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?Z?)"),  # ISO / Rust / Django
    re.compile(r"^\[(\d{2}/[A-Za-z]{3}/\d{4}[ :]\d{2}:\d{2}:\d{2})"),  # apache-ish access
)

# A level token sitting in a `[...]` bracket or as a `LEVEL:` / `LEVEL ` prefix
# within the first stretch of the (timestamp-stripped) message.
_LEVEL_SCAN = re.compile(
    r"^[\[\s]*([A-Za-z]+)\b|\b([A-Za-z]+)\]", re.ASCII
)

# A leading tag: `[label]` or `Label:` / `SYSERR:` at message start.
_TAG_BRACKET = re.compile(r"^\[([A-Za-z][\w.\-]{0,31})\]")
_TAG_COLON = re.compile(r"^([A-Za-z][\w.\-]{0,31}):(?:\s|$)")


def _extract_ts(line):
    for pat in _TS_PATTERNS:
        m = pat.match(line)
        if m:
            return m.group(1), line[m.end():].lstrip()
    return None, line


def _classify_level(rest):
    """Find an explicit level token near the start of `rest`. Returns a level or
    None. Scans the first few whitespace/bracket-delimited tokens only."""
    head = rest[:48]
    # Bracketed level, e.g. "[INFO] ..." or Rust "...Z INFO] ...".
    for tok in re.findall(r"[A-Za-z]+", head):
        norm = _LEVEL_TOKENS.get(tok.lower())
        if norm:
            # Only accept if the token is a standalone level marker, not a word
            # inside prose: require it to be bracketed, colon-suffixed, or the
            # very first token.
            if (
                re.search(rf"\[{tok}\]", head)
                or re.search(rf"\b{tok}\b\s*[\]:]", head)
                or re.search(rf"^\W*{tok}\b", head)
            ):
                return norm
        # Stop scanning once we're clearly into message prose.
        if len(tok) > 12:
            break
    return None


def _extract_tag(rest):
    m = _TAG_BRACKET.match(rest)
    if m:
        return m.group(1)
    m = _TAG_COLON.match(rest)
    if m:
        tag = m.group(1)
        # Don't treat a bare level word ("ERROR:") as a tag — it's the level.
        if tag.lower() not in _LEVEL_TOKENS:
            return tag
    return None


def parse_log(text, source=""):
    """Parse raw log text into structured entries plus filter facets.

    Returns a dict: ``{entries, levels, tags, timeframe, count}`` where each
    entry is ``{i, ts, level, tag, text}`` (``text`` is the full original line,
    kept verbatim for search and copy)."""
    entries = []
    level_counts = {lvl: 0 for lvl in LEVELS}
    tag_counts = {}
    first_ts = last_ts = None
    prev_ts = None

    lines = text.split("\n")
    # A trailing newline yields a final empty element — drop it, keep interior blanks.
    if lines and lines[-1] == "":
        lines.pop()

    for i, line in enumerate(lines):
        ts, rest = _extract_ts(line)
        if ts is not None:
            display_ts = ts
            prev_ts = ts
            if first_ts is None:
                first_ts = ts
            last_ts = ts
        else:
            display_ts = prev_ts

        if ts is None and line[:1].isspace():
            # Indented continuation (traceback body, wrapped C output) — no level
            # of its own; it belongs to the entry above it.
            level = "log"
            tag = None
        else:
            # A real entry — even without a timestamp (Django console lines are
            # often bare "LEVEL message"). Classify from an explicit token only.
            level = _classify_level(rest) or "log"
            tag = _extract_tag(rest)

        level_counts[level] += 1
        if tag:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

        entries.append(
            {"i": i, "ts": display_ts, "level": level, "tag": tag, "text": line}
        )

    tags = [
        {"name": name, "count": tag_counts[name]}
        for name in sorted(tag_counts, key=lambda n: (-tag_counts[n], n.lower()))
    ]
    return {
        "entries": entries,
        "levels": {lvl: level_counts[lvl] for lvl in LEVELS if level_counts[lvl]},
        "tags": tags,
        "timeframe": {"start": first_ts, "end": last_ts},
        "count": len(entries),
    }
