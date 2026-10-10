"""Pure helpers for per-user source preference cookie handling.

Cookie format: URI-encoded source names joined by ','. The cookie stores the
DESELECTED set, so an absent/empty cookie means "all sources selected". This
lets newly-added sources appear by default and keeps the cookie small.
"""

from urllib.parse import unquote


EXCLUDED_SOURCES_COOKIE = 'excluded_sources'
EXCLUDED_SOURCES_MAX_AGE = 365 * 24 * 60 * 60


def parse_excluded_sources(raw, lang_sources):
    """Return a set of excluded source names valid for the current language.

    Args:
        raw: raw cookie string (may be None, empty, or malformed).
        lang_sources: list of (name, bias) tuples for the current language.

    Returns:
        set of source names that are present in ``lang_sources``.
    """
    valid_names = {name for name, _bias in lang_sources}
    excluded = set()
    if not raw:
        return excluded
    try:
        for segment in raw.split(','):
            segment = segment.strip()
            if not segment:
                continue
            try:
                name = unquote(segment)
            except Exception:
                continue
            name = name.strip()
            if name in valid_names:
                excluded.add(name)
    except Exception:
        # Malformed cookie (e.g. unhashable, very long) -> treat as all selected
        return set()
    return excluded


def compute_effective_sources(selected_sources, excluded):
    """Return selected_sources with excluded names removed, preserving order."""
    excluded_set = set(excluded)
    return [s for s in selected_sources if s not in excluded_set]


def encode_excluded_sources(excluded_names):
    """Encode a set/list of excluded source names for the cookie value."""
    from urllib.parse import quote
    return ','.join(quote(name, safe='') for name in sorted(excluded_names))
