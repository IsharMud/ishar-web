"""Shared user-input text hygiene for site-owned submission surfaces."""

# Bidirectional/direction-override codepoints that can spoof displayed order —
# stripped to match the game's Rust `sanitize_text` (feedback.rs).
_BIDI_OVERRIDES = frozenset(
    chr(cp) for cp in list(range(0x202A, 0x202F)) + list(range(0x2066, 0x206A))
)


def clean_text(text, limit) -> str:
    """Strip control + bidi-override characters and truncate — mirrors
    `sanitize_text`."""
    if not text:
        return ""
    cleaned = "".join(
        ch for ch in str(text)
        if (ch in ("\n", "\t") or ord(ch) >= 0x20) and ch not in _BIDI_OVERRIDES
    ).strip()
    if len(cleaned) > limit:
        cleaned = cleaned[:limit].rstrip()
    return cleaned
