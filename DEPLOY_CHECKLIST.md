# Deployment Checklist for 24HourWire
# This file serves as a mandatory reminder to TEST BEFORE DEPLOYING

## ⚠️ CRITICAL: NEVER DEPLOY WITHOUT TESTING ⚠️

### Pre-Deployment Checklist (MANDATORY)

Before every commit/push, you MUST:

- [ ] 1. Run Django system checks: `python manage.py check`
- [ ] 2. Run categorization tests: `python manage.py test_categories`
- [ ] 3. Run Django unit tests: `python manage.py test`
- [ ] 4. Check for syntax errors in modified Python files
- [ ] 5. Verify templates compile correctly
- [ ] 6. Test locally if possible (runserver and click around)

### Test Results Documentation

**Last Tested:** ___________

**Test Results:**
- [ ] Django system check: PASSED
- [ ] Categorization tests: ___/___ passed
- [ ] Unit tests: PASSED
- [ ] No syntax errors: CONFIRMED
- [ ] Templates valid: CONFIRMED

**Tested By:** ___________

### Deployment Log

| Date | Commit | Tests Passed | Notes |
|------|--------|--------------|-------|
|      |        |              |       |

## Remember

1. **ALWAYS test before committing**
2. **ALWAYS verify test results before pushing**
3. **If tests fail, DO NOT deploy**

## Common Test Commands

```bash
# Check Django configuration
python manage.py check

# Run categorization tests (102 test cases across 13 languages)
python manage.py test_categories

# Run Django unit tests
python manage.py test

# Check fetch status (on production)
python manage.py check_fetch_status
```

## Emergency Contacts/Issues

If deployment fails:
1. Check Render dashboard logs
2. Check fetch_news.log on server
3. Rollback to last known good commit if needed
