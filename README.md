# 24HourWire

A minimal news aggregator that pulls stories from wire services and allows users to filter by source bias.

## Live Site

**https://two4hourwire.onrender.com**

## Features

- Aggregates news from 37+ sources
- Shows bias ratings for each source
- Filter by bias category (Center, Left, Right)
- **Regional categorization** - Language-specific regional categories:
  - English: United States, United Kingdom, Europe, Asia-Pacific
  - Spanish: España, México, Latinoamérica, Europa
  - German: Deutschland, Österreich, Schweiz, Europa
  - And 10 more languages with region-appropriate categories
- Categorizes stories by topic (World, Politics, Business, Tech, Science, Health, Sports)
- Auto-fetches news every 15 minutes
- "Most Covered" tab shows stories in 2+ sources
- Privacy-first (no cookies, no tracking)
- Legal protection (Terms, Privacy Policy)

## Tech Stack

- Python/Django
- PostgreSQL (production) / SQLite (development)
- Whitenoise for static files
- Gunicorn for production server

## Deployment

See [DEPLOY.md](DEPLOY.md) for deployment instructions.

## Recent Changes

### Regional Categories (April 2025)

**Breaking Change**: The "US" category has been replaced with language-specific regional categories.

Each language now has region-appropriate categories:
- **English**: United States, United Kingdom, Europe, Asia-Pacific
- **Spanish**: España, México, Latinoamérica, Europa  
- **German**: Deutschland, Österreich, Schweiz, Europa
- **French**: France, Belgique, Suisse, Europe
- **Italian**: Italia, Europa
- **Portuguese**: Brasil, Portugal
- **Japanese**: Japan, Asia
- **Korean**: Korea, Asia
- **Chinese**: China, Hong Kong, Taiwan, Asia
- **Russian**: Russia, CIS, Europe
- **Arabic**: Gulf, Egypt, Levant, Maghreb
- **Hindi**: India, South Asia
- **Turkish**: Turkey, Balkans

**Migration Notes**:
- **New stories** will be categorized with the new regional system
- **Existing stories** retain their old categories ("us" becomes "united-states" for English, or language-appropriate regional category)
- The template automatically hides categories with 0 stories
- Categories now use weighted keyword scoring for better accuracy

## License

MIT
