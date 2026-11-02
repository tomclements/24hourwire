# Amazon seasonal product recommendations for 24HourWire affiliate links.
# This is the single seasonal product list used across every English tab
# and load-more slot. Each entry uses a generic Amazon search query only;
# no prices, ratings, or ASINs are stored here; images are optional (see below).
#
# Images may be either a self-hosted static file ('image': 'products/x.jpg',
# under news/static/news/img/) or a SiteStripe-issued https 'image_url'; if
# both are set, the local file wins. Only SiteStripe-issued Amazon image URLs are
# allowed; copy them from SiteStripe's Image tab while signed in with tag
# 24hourwire06-20.
#
# When an entry carries an optional 'image_url', it MUST be copied from the
# Amazon Associates SiteStripe "Image" tab while signed in with the
# 24hourwire06-20 tag. Never paste other Amazon image URLs or hotlink images
# that were not obtained through SiteStripe for this associate account.
# If a SiteStripe image URL is used, set 'image_url' in the entry and leave
# 'image' empty; display_image_url() will serve it only if its host is in the
# allowlist.
#
# When using self-hosted images, set 'image' to a path like 'products/x.jpg'
# (relative to news/static/news/img/); display_image_url() resolves it through
# Django's static files.
SEASON = 'holiday-2026'

PRODUCTS = [
    {
        'name': 'Kindle Paperwhite',
        'search_query': 'Kindle Paperwhite',
        'description': 'A waterproof e-reader perfect for book lovers.',
    },
    {
        'name': 'Echo Dot',
        'search_query': 'Echo Dot smart speaker',
        'description': 'A compact smart speaker for music, timers, and news.',
    },
    {
        'name': 'Apple AirPods',
        'search_query': 'Apple AirPods wireless earbuds',
        'description': 'Popular wireless earbuds for calls and music on the go.',
    },
    {
        'name': 'Stanley Quencher Tumbler',
        'search_query': 'Stanley Quencher tumbler',
        'description': 'A viral insulated tumbler that keeps drinks cold for hours.',
    },
    {
        'name': 'LEGO Creator Set',
        'search_query': 'LEGO Creator building set',
        'description': 'A creative building set that makes a great holiday gift.',
    },
    {
        'name': 'Instant Pot Duo',
        'search_query': 'Instant Pot Duo pressure cooker',
        'description': 'A multi-functional pressure cooker for easy weeknight meals.',
    },
    {
        'name': 'Fire TV Stick',
        'search_query': 'Amazon Fire TV Stick streaming',
        'description': 'A streaming media player for movies, shows, and apps.',
    },
    {
        'name': 'Ninja Air Fryer',
        'search_query': 'Ninja air fryer',
        'description': 'A countertop air fryer for crispy favorites with less oil.',
    },
    {
        'name': 'Owala FreeSip Water Bottle',
        'search_query': 'Owala FreeSip water bottle',
        'description': 'A leak-proof bottle with a built-in straw for everyday hydration.',
    },
    {
        'name': 'Weighted Blanket',
        'search_query': 'weighted blanket adults',
        'description': 'A cozy weighted blanket for relaxation and better sleep.',
    },
    {
        'name': 'Roku Streaming Stick',
        'search_query': 'Roku Streaming Stick',
        'description': 'A portable streaming device for HD entertainment.',
    },
    {
        'name': 'Tile Mate Tracker',
        'search_query': 'Tile Mate Bluetooth tracker',
        'description': 'A small Bluetooth tracker for keys, bags, and wallets.',
    },
    {
        'name': 'Anker Portable Charger',
        'search_query': 'Anker portable charger power bank',
        'description': 'A reliable power bank to keep devices charged on the go.',
    },
    {
        'name': 'Hydro Flask Bottle',
        'search_query': 'Hydro Flask water bottle',
        'description': 'A durable insulated bottle for hot or cold drinks.',
    },
    {
        'name': 'Candle Gift Set',
        'search_query': 'scented candle gift set',
        'description': 'A set of relaxing scented candles for the holiday season.',
    },
    {
        'name': 'Fitbit Inspire',
        'search_query': 'Fitbit Inspire fitness tracker',
        'description': 'A simple fitness tracker for steps, sleep, and workouts.',
    },
]
