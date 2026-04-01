"""
Standalone categorization module without Django dependencies.

This module can be imported in cron jobs and other contexts without
requiring Django to be fully configured.
"""

from news.languages import CATEGORY_KEYWORDS_WEIGHTED, EXCLUSION_RULES


def check_exclusion(title_lower, category, keyword):
    """Check if a keyword match should be excluded based on context."""
    if category in EXCLUSION_RULES and keyword in EXCLUSION_RULES[category]:
        for exclusion_phrase in EXCLUSION_RULES[category][keyword]:
            if exclusion_phrase in title_lower:
                return True
    return False


def categorize_story(title, language='en'):
    """Categorize a story using weighted keyword scoring.
    
    Returns the single best category based on highest score.
    """
    title_lower = title.lower()
    # CATEGORY_KEYWORDS_WEIGHTED is already the English keywords dict
    # (not a {language: {category: weights}} structure)
    weighted_keywords = CATEGORY_KEYWORDS_WEIGHTED
    
    category_scores = {}
    
    for category, weights in weighted_keywords.items():
        score = 0
        # High weight keywords (3 points)
        for keyword in weights.get('high', []):
            if keyword in title_lower and not check_exclusion(title_lower, category, keyword):
                score += 3
        # Medium weight keywords (2 points)
        for keyword in weights.get('medium', []):
            if keyword in title_lower and not check_exclusion(title_lower, category, keyword):
                score += 2
        # Low weight keywords (1 point)
        for keyword in weights.get('low', []):
            if keyword in title_lower and not check_exclusion(title_lower, category, keyword):
                score += 1
        
        if score > 0:
            category_scores[category] = score
    
    # Return category with highest score, or 'world' if no matches
    if category_scores:
        return max(category_scores, key=category_scores.get)
    return 'world'


def get_story_categories(title, language='en'):
    """Get all applicable categories for a story using weighted scoring.
    
    Returns categories with score >= 3 (high confidence) or top 2 categories.
    """
    title_lower = title.lower()
    # CATEGORY_KEYWORDS_WEIGHTED is already the English keywords dict
    weighted_keywords = CATEGORY_KEYWORDS_WEIGHTED
    
    category_scores = {}
    
    for category, weights in weighted_keywords.items():
        score = 0
        # High weight keywords (3 points)
        for keyword in weights.get('high', []):
            if keyword in title_lower and not check_exclusion(title_lower, category, keyword):
                score += 3
        # Medium weight keywords (2 points)
        for keyword in weights.get('medium', []):
            if keyword in title_lower and not check_exclusion(title_lower, category, keyword):
                score += 2
        # Low weight keywords (1 point)
        for keyword in weights.get('low', []):
            if keyword in title_lower and not check_exclusion(title_lower, category, keyword):
                score += 1
        
        if score > 0:
            category_scores[category] = score
    
    # Filter categories: require score >= 3 OR take top 2 categories
    if not category_scores:
        return ['world']
    
    # Get categories with high confidence (score >= 3)
    high_confidence = [cat for cat, score in category_scores.items() if score >= 3]
    if high_confidence:
        return high_confidence
    
    # Otherwise take top 2 categories
    sorted_cats = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
    return [cat for cat, _ in sorted_cats[:2]]
