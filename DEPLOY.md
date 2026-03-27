# 24HourWire Deployment Guide

## Render Deployment (Recommended)

### Prerequisites
1. GitHub account
2. Render account (paid plan for cron jobs)
3. PostgreSQL database (Render provides PostgreSQL)

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/24hourwire.git
   git push -u origin main
   ```

2. **Create PostgreSQL Database on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "PostgreSQL"
   - Choose "Free" plan
   - Name: `24hourwire-db`
   - Copy the "External Database URL"

3. **Deploy Web Service on Render**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Name: `two4hourwire` (or `24hourwire` if available)
     - Region: Choose closest to you
     - Branch: `main`
     - Runtime: `Python 3`
     - Build Command: `./build.sh`
     - Start Command: `gunicorn core.wsgi:application`
   
4. **Set Environment Variables**
   ```
   SECRET_KEY=<generate-a-new-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=two4hourwire.onrender.com
   DATABASE_ENGINE=django.db.backends.postgresql
   DATABASE_URL=<your-postgresql-external-url>
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy

### Cron Job for Auto-Fetch

Render has built-in cron jobs (paid plans). To fetch news every 15 minutes:

1. Go to your [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Cron Job"
3. Configure:
   - **Name**: `24hourwire-fetch-news`
   - **Region**: Same as your web service
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Command**: `python manage.py fetch_news`
   - **Schedule**: `*/15 * * * *` (every 15 minutes)
4. Set the same environment variables as your web service (`DATABASE_*`, `SECRET_KEY`)
5. Click "Create Cron Job"

The cron job runs `fetch_news` directly — no web endpoint needed.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | (must be set in production) |
| DEBUG | Enable debug mode | True |
| ALLOWED_HOSTS | Comma-separated domains | localhost,127.0.0.1 |
| DATABASE_ENGINE | Database backend | django.db.backends.sqlite3 |
| DATABASE_NAME | Database name | db.sqlite3 |
| DATABASE_USER | Database user | (empty) |
| DATABASE_PASSWORD | Database password | (empty) |
| DATABASE_HOST | Database host | (empty) |
| DATABASE_PORT | Database port | (empty) |

## Generate New Secret Key

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
