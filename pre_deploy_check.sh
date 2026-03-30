#!/bin/bash
# Pre-deployment testing script for 24HourWire
# Run this before committing/pushing to catch errors locally

echo "================================"
echo "24HourWire Pre-Deploy Checklist"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. Check if Python is available
echo "1. Checking Python..."
if command_exists python; then
    PYTHON_CMD="python"
elif command_exists python3; then
    PYTHON_CMD="python3"
else
    echo -e "${RED}✗ Python not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found: $PYTHON_CMD${NC}"
echo ""

# 2. Check Django installation
echo "2. Checking Django..."
if $PYTHON_CMD -c "import django" 2>/dev/null; then
    DJANGO_VERSION=$($PYTHON_CMD -c "import django; print(django.__version__)")
    echo -e "${GREEN}✓ Django $DJANGO_VERSION installed${NC}"
else
    echo -e "${RED}✗ Django not installed${NC}"
    echo "   Run: pip install -r requirements.txt"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 3. Check for pending migrations
echo "3. Checking for pending migrations..."
cd "$(dirname "$0")"
MIGRATION_CHECK=$($PYTHON_CMD manage.py showmigrations --plan 2>&1 | grep "\[ \]" | wc -l)
if [ "$MIGRATION_CHECK" -gt 0 ]; then
    echo -e "${YELLOW}⚠ $MIGRATION_CHECK pending migrations found${NC}"
    echo "   Run: python manage.py makemigrations && python manage.py migrate"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}✓ All migrations applied${NC}"
fi
echo ""

# 4. Check for model changes without migrations
echo "4. Checking for model changes without migrations..."
MIGRATION_CHANGES=$($PYTHON_CMD manage.py makemigrations --dry-run --check 2>&1)
if echo "$MIGRATION_CHANGES" | grep -q "No changes detected"; then
    echo -e "${GREEN}✓ No model changes requiring migrations${NC}"
else
    echo -e "${RED}✗ Model changes detected without migrations${NC}"
    echo "   Run: python manage.py makemigrations"
    echo "   Changes:"
    echo "$MIGRATION_CHANGES" | grep -A5 "Migrations for"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 5. Run Django system checks
echo "5. Running Django system checks..."
SYS_CHECK=$($PYTHON_CMD manage.py check --deploy 2>&1)
if echo "$SYS_CHECK" | grep -q "System check identified no issues"; then
    echo -e "${GREEN}✓ Django system checks passed${NC}"
else
    echo -e "${YELLOW}⚠ Django issues found:${NC}"
    echo "$SYS_CHECK" | grep -A2 "WARNINGS\|ERRORS" | head -20
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# 6. Check if server can start (syntax errors, import errors)
echo "6. Testing if Django can start..."
TIMEOUT=10
$PYTHON_CMD manage.py check 2>&1 > /tmp/django_check.log &
PID=$!
sleep 2
if ps -p $PID > /dev/null; then
    kill $PID 2>/dev/null
    wait $PID 2>/dev/null
fi

if grep -q "error\|Error\|ERROR\|Traceback" /tmp/django_check.log; then
    echo -e "${RED}✗ Django failed to start:${NC}"
    cat /tmp/django_check.log | head -30
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓ Django starts successfully${NC}"
fi
echo ""

# 7. Check for syntax errors in Python files
echo "7. Checking for Python syntax errors..."
SYNTAX_ERRORS=0
while IFS= read -r -d '' file; do
    if ! $PYTHON_CMD -m py_compile "$file" 2>/dev/null; then
        echo -e "${RED}✗ Syntax error in: $file${NC}"
        SYNTAX_ERRORS=$((SYNTAX_ERRORS + 1))
    fi
done < <(find . -name "*.py" -type f ! -path "./venv/*" ! -path "./.git/*" ! -path "./__pycache__/*" -print0)

if [ $SYNTAX_ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ No Python syntax errors${NC}"
else
    echo -e "${RED}✗ $SYNTAX_ERRORS Python file(s) with syntax errors${NC}"
    ERRORS=$((ERRORS + SYNTAX_ERRORS))
fi
echo ""

# 8. Check templates for obvious errors
echo "8. Checking Django templates..."
TEMPLATE_ERRORS=0
while IFS= read -r -d '' file; do
    # Check for unclosed tags (basic check)
    if grep -q "{%.*{%" "$file" 2>/dev/null; then
        echo -e "${YELLOW}⚠ Possible template issue in: $file${NC}"
        TEMPLATE_ERRORS=$((TEMPLATE_ERRORS + 1))
    fi
done < <(find . -name "*.html" -type f ! -path "./venv/*" ! -path "./.git/*" -print0)

if [ $TEMPLATE_ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ No obvious template errors${NC}"
else
    echo -e "${YELLOW}⚠ $TEMPLATE_ERRORS potential template issue(s)${NC}"
    WARNINGS=$((WARNINGS + TEMPLATE_ERRORS))
fi
echo ""

# 9. Check for common mistakes in models
echo "9. Checking models for common issues..."
if grep -r "default=False" news/models.py | grep -q "BooleanField"; then
    echo -e "${GREEN}✓ BooleanFields have defaults${NC}"
else
    echo -e "${YELLOW}⚠ Some BooleanFields might be missing defaults${NC}"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# 10. Git status check
echo "10. Checking git status..."
if [ -d .git ]; then
    UNCOMMITTED=$(git status --porcelain | wc -l)
    if [ $UNCOMMITTED -gt 0 ]; then
        echo -e "${YELLOW}⚠ $UNCOMMITTED uncommitted change(s)${NC}"
        git status --short
    else
        echo -e "${GREEN}✓ All changes committed${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Not a git repository${NC}"
fi
echo ""

# Summary
echo "================================"
echo "SUMMARY"
echo "================================"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED${NC}"
    echo "Safe to deploy!"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ $WARNINGS warning(s) found${NC}"
    echo "Review warnings, but should be safe to deploy"
    exit 0
else
    echo -e "${RED}✗ $ERRORS error(s) found${NC}"
    [ $WARNINGS -gt 0 ] && echo -e "${YELLOW}⚠ $WARNINGS warning(s)${NC}"
    echo "Fix errors before deploying!"
    exit 1
fi