# 24HourWire

A minimal news aggregator that pulls stories from wire services and allows users to filter by source bias.

## Live Site

**https://two4hourwire.onrender.com**

## Features

- Aggregates news from 37+ sources
- Shows bias ratings for each source
- Filter by bias category (Center, Left, Right)
- Categorizes stories (World, US, Politics, Business, Tech, Science, Health, Sports)
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

## License

MIT
