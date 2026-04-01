"""Test cases for story categorization system.

Run with: python manage.py test_categories
"""

TEST_CASES = [
    # Format: (title, expected_categories, notes)
    
    # US Politics
    ("Biden signs executive order on climate change", ["politics", "us"], "White House action"),
    ("Supreme Court rules on voting rights case", ["politics", "us"], "Supreme Court + federal"),
    ("FBI investigates cyberattack on government servers", ["politics", "technology", "us"], "FBI + tech"),
    
    # International Politics
    ("UK Parliament debates Brexit trade deal", ["politics", "world"], "Parliament + Brexit"),
    ("Kremlin denies involvement in election interference", ["politics", "world"], "International politics"),
    ("Prime Minister calls snap election amid crisis", ["politics", "world"], "International election"),
    
    # Business
    ("Fed raises interest rates to combat inflation", ["business"], "Federal Reserve action"),
    ("Tech startup raises $50M in Series A funding", ["business", "technology"], "Startup funding"),
    ("Wall Street reacts to quarterly earnings reports", ["business"], "Finance"),
    
    # Technology
    ("OpenAI releases new GPT model", ["technology"], "AI/tech"),
    ("Apple unveils augmented reality headset", ["technology"], "Tech hardware"),
    ("Tesla announces self-driving car update", ["technology"], "Autonomous vehicles"),
    ("Cybersecurity firm reports major data breach", ["technology"], "Security"),
    
    # Science
    ("NASA discovers water on Mars", ["science"], "Space"),
    ("Study finds link between diet and longevity", ["science", "health"], "Research + health"),
    ("Researchers publish breakthrough in quantum computing", ["science", "technology"], "Quantum + tech"),
    
    # Health
    ("FDA approves new cancer treatment drug", ["health"], "Medical approval"),
    ("Hospital reports surge in flu cases", ["health"], "Healthcare"),
    ("WHO declares end of pandemic emergency", ["health", "world"], "WHO + global health"),
    
    # Sports
    ("NBA playoffs: Lakers advance to finals", ["sports"], "Basketball"),
    ("World Cup final draws record viewership", ["sports"], "Soccer"),
    ("Olympics committee announces host city", ["sports"], "Olympics"),
    
    # World News (should NOT be tagged US)
    ("South Africa considers fuel levy cut", ["world"], "Should NOT be US (was false positive)"),
    ("South Korea chipmakers report strong earnings", ["business", "world"], "Should NOT be US (was false positive)"),
    ("Earthquake strikes Japan, tsunami warning issued", ["world"], "Natural disaster"),
    ("European Union imposes new sanctions on Russia", ["world", "business"], "Geopolitics"),
    
    # Entertainment
    ("Netflix releases new documentary series", ["entertainment"], "Streaming"),
    ("Oscar nominations announced", ["entertainment"], "Awards"),
    ("Taylor Swift announces world tour dates", ["entertainment"], "Music"),
    
    # Edge cases (should be carefully categorized)
    ("Virus spreads through computer networks", ["technology"], "Computer virus (NOT health)"),
    ("Election campaign targets young voters", ["politics"], "Campaign (NOT sports draft)"),
    ("Startup develops AI for healthcare", ["technology", "health"], "Tech + health crossover"),
    ("Trade war escalates between US and China", ["business", "world", "us"], "Trade + geopolitics"),
]

# Categories that should never appear together (optional validation)
CONFLICTING_CATEGORIES = [
    ("us", "world"),  # A story shouldn't be both US and World
]
