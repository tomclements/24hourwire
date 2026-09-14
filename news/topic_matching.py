"""DB-agnostic topic title matching with tiered keyword scores.

Mirrors news.categorization patterns (keyword_in_title word boundaries)
so SQLite tests and Postgres production stay consistent — no Postgres
\\b / __iregex.

Acceptance rule (chosen, consistent everywhere):
  Accept if score >= min_score (default 2).

Scoring:
  - anchors: +3 each matched term
  - medium:  +2 each matched term
  - weak:    +1 each matched term, ONLY if >=1 anchor already matched
  - any negative hit -> reject immediately
  - deny_categories: reject when story.category is in the list

Because each anchor contributes +3, a single anchor always meets the
default min_score of 2. Weak tokens alone never accept (they require an
anchor first and only boost an already-qualifying or near score).

Backward compatibility:
  If match_rules is empty/missing, legacy flat `keywords` are treated as
  medium-only (one keyword match => score 2 => accept). Matcher prefers
  match_rules when present; keywords remain the union for admin/legacy.
"""

from __future__ import annotations

from django.db.models import Q

from news.categorization import keyword_in_title


DEFAULT_MIN_SCORE = 2

# Shared sports false-positive blockers for geopolitics topics
GEOPOLITICS_NEGATIVES = [
    'packers',
    'nfl',
    'nba',
    'mlb',
    'premier league',
    'quarterback',
    'jordan love',
    'michael jordan',
]


def _as_list(value):
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        return [str(v).strip().lower() for v in value if str(v).strip()]
    return []


def resolve_match_rules(topic) -> dict:
    """Normalize match_rules from a Topic (or dict-like) instance.

    Prefer topic.match_rules when non-empty. Otherwise derive medium-only
    rules from legacy topic.keywords.
    """
    raw = getattr(topic, 'match_rules', None) or {}
    if isinstance(raw, dict) and any(
        raw.get(k) for k in ('anchors', 'medium', 'weak', 'negatives', 'deny_categories')
    ):
        return {
            'anchors': _as_list(raw.get('anchors')),
            'medium': _as_list(raw.get('medium')),
            'weak': _as_list(raw.get('weak')),
            'negatives': _as_list(raw.get('negatives')),
            'deny_categories': _as_list(raw.get('deny_categories')),
            'min_score': int(raw.get('min_score') or DEFAULT_MIN_SCORE),
        }

    # Legacy: flat keywords act as medium-only
    keywords = _as_list(getattr(topic, 'keywords', None) or [])
    return {
        'anchors': [],
        'medium': keywords,
        'weak': [],
        'negatives': [],
        'deny_categories': [],
        'min_score': DEFAULT_MIN_SCORE,
    }


def keywords_union_from_rules(rules: dict) -> list:
    """Union of positive terms for legacy keywords field / SQL prefilter."""
    seen = set()
    out = []
    for key in ('anchors', 'medium', 'weak'):
        for term in rules.get(key) or []:
            if term not in seen:
                seen.add(term)
                out.append(term)
    return out


def score_title(title: str, rules: dict, category: str | None = None) -> tuple[bool, int]:
    """Score a title against match rules. Returns (accepted, score)."""
    if not title:
        return False, 0

    title_lower = title.lower()
    min_score = int(rules.get('min_score') or DEFAULT_MIN_SCORE)

    deny = rules.get('deny_categories') or []
    if category and deny and category.lower() in deny:
        return False, 0

    for neg in rules.get('negatives') or []:
        if keyword_in_title(neg, title_lower):
            return False, 0

    anchors_hit = 0
    score = 0

    for term in rules.get('anchors') or []:
        if keyword_in_title(term, title_lower):
            anchors_hit += 1
            score += 3

    for term in rules.get('medium') or []:
        if keyword_in_title(term, title_lower):
            score += 2

    if anchors_hit >= 1:
        for term in rules.get('weak') or []:
            if keyword_in_title(term, title_lower):
                score += 1

    accepted = score >= min_score
    return accepted, score


def title_matches_rules(title: str, rules: dict, category: str | None = None) -> bool:
    accepted, _ = score_title(title, rules, category=category)
    return accepted


def story_matches_topic(story, topic) -> bool:
    """True if story title matches topic under shared acceptance rules."""
    rules = resolve_match_rules(topic)
    category = getattr(story, 'category', None) or None
    title = getattr(story, 'title', '') or ''
    return title_matches_rules(title, rules, category=category)


def positive_terms_for_topic(topic) -> list:
    """All positive keyword strings used for cheap SQL prefilter."""
    rules = resolve_match_rules(topic)
    terms = keywords_union_from_rules(rules)
    # Also include legacy keywords in case match_rules omits some
    for kw in _as_list(getattr(topic, 'keywords', None) or []):
        if kw not in terms:
            terms.append(kw)
    return terms


def build_prefilter_q(topic):
    """Cheap title__icontains OR across positive terms (candidate narrowing).

    Final acceptance is always decided in Python via score_title.
    Returns None when there are no terms (match nothing).
    """
    terms = positive_terms_for_topic(topic)
    if not terms:
        return None
    q = Q()
    for term in terms:
        q |= Q(title__icontains=term)
    return q
