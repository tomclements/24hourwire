# Testing & Deployment Workflow

## Before Every Deployment - MANDATORY CHECKLIST

### 1. Run Pre-Deploy Checks
```bash
# Make the script executable (first time only)
chmod +x pre_deploy_check.sh

# Run the checks
./pre_deploy_check.sh
```

**If this script reports ERRORS, DO NOT DEPLOY. Fix them first.**

### 2. Test Database Changes (CRITICAL)

**For ANY model changes:**
```bash
# 1. Create migrations
python manage.py makemigrations

# 2. Apply migrations locally
python manage.py migrate

# 3. Test the site locally
python manage.py runserver

# 4. Verify no errors in browser at http://localhost:8000
```

**NEVER deploy without running migrations locally first!**

### 3. Test Key Functionality Locally

```bash
# Start local server
python manage.py runserver

# Test these URLs in browser:
# - http://localhost:8000/ (home page)
# - http://localhost:8000/about/
# - http://localhost:8000/terms/
# - http://localhost:8000/privacy/

# Check browser console for JavaScript errors
```

### 4. Run Management Commands Locally

```bash
# Test fetch_news (run for just one language to save time)
python manage.py fetch_news --language en

# If that works, test the full fetch
python manage.py fetch_news
```

### 5. Commit All Changes

```bash
git status                    # Check what's changed
git add -A                    # Stage all changes
git commit -m "Description"   # Commit with good message
git push origin main          # Push to GitHub
```

### 6. Deploy to Render

```bash
# Trigger deploy via CLI
RENDER_API_KEY=your_key ./render.exe deploys create srv-d72akb4g9agc7393r55g --confirm

# Or let it auto-deploy from GitHub push
```

### 7. Verify Deployment

```bash
# Check deploy status
./render.exe deploys list srv-d72akb4g9agc7393r55g

# Check for errors
./render.exe logs -r srv-d72akb4g9agc7393r55g --tail 20
```

## Common Issues & Solutions

### Issue: "No module named 'X'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Table 'news_story' doesn't exist"
**Solution:**
```bash
python manage.py migrate
```

### Issue: "Column 'tweeted' doesn't exist"
**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: 500 errors after deployment
**Check:**
1. Did you run migrations locally first?
2. Did the migration file get committed?
3. Check Render logs: `./render.exe logs -r srv-d72akb4g9agc7393r55g`

## Database Migration Rules

**ALWAYS:**
- ✓ Create migrations before committing model changes
- ✓ Run migrations locally to test
- ✓ Commit the migration files to git
- ✓ Test the site locally after migrations

**NEVER:**
- ✗ Commit model changes without migrations
- ✗ Delete migration files manually
- ✗ Edit migration files unless you know what you're doing

## Testing Checklist Template

Copy this into your commit message:

```
[ ] Ran pre_deploy_check.sh - no errors
[ ] Tested migrations locally
[ ] Site loads without 500 errors locally
[ ] Tested fetch_news command locally
[ ] All changes committed
[ ] Pushed to GitHub
[ ] Deployed to Render successfully
[ ] Verified site works in production
```

## Emergency Rollback

If deployment breaks:

```bash
# Find previous working deploy
./render.exe deploys list srv-d72akb4g9agc7393r55g

# Rollback to previous version
./render.exe deploys rollback srv-d72akb4g9agc7393r55g <deploy-id>
```