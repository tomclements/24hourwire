"""
Standalone categorization module without Django dependencies.

This module can be imported in cron jobs and other contexts without
requiring Django to be fully configured.
"""

import re
from news.languages import LANGUAGE_CATEGORY_KEYWORDS_WEIGHTED, LANGUAGE_EXCLUSION_RULES


def check_exclusion(title_lower, category, keyword, language='en'):
    """Check if a keyword match should be excluded based on context."""
    exclusion_rules = LANGUAGE_EXCLUSION_RULES.get(language, LANGUAGE_EXCLUSION_RULES.get('en', {}))
    if category in exclusion_rules and keyword in exclusion_rules[category]:
        for exclusion_phrase in exclusion_rules[category][keyword]:
            if exclusion_phrase in title_lower:
                return True
    return False


def keyword_in_title(keyword, title_lower):
    """Check if keyword appears as a whole word in title.
    
    Uses word boundaries to prevent false matches:
    - 'cia' won't match 'commercial'
    - 'ai' won't match 'raises'
    - 'fed' won't match 'nfl' (wait, that would need to be 'nfl' matching 'fed' inside it)
    
    Handles multi-word keywords like 'white house' and 'stock market'.
    """
    # Escape special regex characters in keyword
    escaped_keyword = re.escape(keyword)
    # Use word boundaries for single words, but for multi-word phrases
    # we check for the phrase surrounded by word boundaries or string boundaries
    if ' ' in keyword:
        # Multi-word phrase - check it appears as-is
        pattern = r'(?:^|[^a-z])' + escaped_keyword + r'(?:[^a-z]|$)'
    else:
        # Single word - use word boundaries
        pattern = r'\b' + escaped_keyword + r'\b'
    
    return re.search(pattern, title_lower) is not None


def categorize_story(title, language='en'):
    """Categorize a story using weighted keyword scoring.
    
    Returns the single best category based on highest score.
    Uses language-specific keywords if available, falls back to English.
    """
    title_lower = title.lower()
    # Get language-specific weighted keywords, fall back to English
    weighted_keywords = LANGUAGE_CATEGORY_KEYWORDS_WEIGHTED.get(
        language, 
        LANGUAGE_CATEGORY_KEYWORDS_WEIGHTED.get('en', {})
    )
    
    category_scores = {}
    
    for category, weights in weighted_keywords.items():
        score = 0
        # High weight keywords (3 points)
        for keyword in weights.get('high', []):
            if keyword_in_title(keyword, title_lower) and not check_exclusion(title_lower, category, keyword, language):
                score += 3
        # Medium weight keywords (2 points)
        for keyword in weights.get('medium', []):
            if keyword_in_title(keyword, title_lower) and not check_exclusion(title_lower, category, keyword, language):
                score += 2
        # Low weight keywords (1 point)
        for keyword in weights.get('low', []):
            if keyword_in_title(keyword, title_lower) and not check_exclusion(title_lower, category, keyword, language):
                score += 1
        
        if score > 0:
            category_scores[category] = score
    
    # Return category with highest score, or 'world' if no matches
    if category_scores:
        return max(category_scores, key=category_scores.get)
    return 'world'


def get_story_categories(title, language='en'):
    """Get all applicable categories for a story using weighted scoring.
    
    Returns categories with score >= 3 (high confidence) OR score >= 2 (medium confidence).
    Regional categories (united-states, europe, etc.) can be combined with topic categories.
    Uses language-specific keywords if available, falls back to English.
    """
    title_lower = title.lower()
    # Get language-specific weighted keywords, fall back to English
    weighted_keywords = LANGUAGE_CATEGORY_KEYWORDS_WEIGHTED.get(
        language, 
        LANGUAGE_CATEGORY_KEYWORDS_WEIGHTED.get('en', {})
    )
    
    category_scores = {}
    
    for category, weights in weighted_keywords.items():
        score = 0
        # High weight keywords (3 points)
        for keyword in weights.get('high', []):
            if keyword_in_title(keyword, title_lower) and not check_exclusion(title_lower, category, keyword, language):
                score += 3
        # Medium weight keywords (2 points)
        for keyword in weights.get('medium', []):
            if keyword_in_title(keyword, title_lower) and not check_exclusion(title_lower, category, keyword, language):
                score += 2
        # Low weight keywords (1 point)
        for keyword in weights.get('low', []):
            if keyword_in_title(keyword, title_lower) and not check_exclusion(title_lower, category, keyword, language):
                score += 1
        
        if score > 0:
            category_scores[category] = score
    
    # Filter categories: include those with score >= 2 (medium confidence or higher)
    if not category_scores:
        return ['world']
    
    # Get categories with at least medium confidence (score >= 2)
    qualifying = [cat for cat, score in category_scores.items() if score >= 2]
    if qualifying:
        return qualifying
    
    # If nothing qualifies with score >= 2, take top category only
    sorted_cats = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
    return [sorted_cats[0][0]] if sorted_cats else ['world']
