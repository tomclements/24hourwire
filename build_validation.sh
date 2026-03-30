#!/bin/bash
# Pre-deployment validation script for Render
# This runs during the build phase to catch errors before deployment
# Place this in your repository root and call it from render.yaml or as a build command

set -e  # Exit on error

echo "================================"
echo "24HourWire Build Validation"
echo "================================"
echo ""

ERRORS=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to log errors
error() {
    echo -e "${RED}✗ $1${NC}"
    ERRORS=$((ERRORS + 1))
}

# Function to log success
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to log warnings
warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

echo "1. Checking Python environment..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    error "Python not found"
    exit 1
fi
success "Python found: $PYTHON_CMD"

echo ""
echo "2. Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -q -r requirements.txt
    success "Dependencies installed"
else
    error "requirements.txt not found"
    exit 1
fi

echo ""
echo "3. Checking for syntax errors..."
SYNTAX_ERRORS=0
while IFS= read -r -d '' file; do
    if ! $PYTHON_CMD -m py_compile "$file" 2>/dev/null; then
        error "Syntax error in: $file"
        SYNTAX_ERRORS=$((SYNTAX_ERRORS + 1))
    fi
done < <(find . -name "*.py" -type f ! -path "./venv/*" ! -path "./.git/*" ! -path "./__pycache__/*" -print0)

if [ $SYNTAX_ERRORS -eq 0 ]; then
    success "No Python syntax errors"
else
    error "$SYNTAX_ERRORS Python file(s) with syntax errors"
fi

echo ""
echo "4. Checking for missing migrations..."
MIGRATION_CHECK=$($PYTHON_CMD manage.py makemigrations --dry-run --check 2>&1 || true)
if echo "$MIGRATION_CHECK" | grep -q "No changes detected"; then
    success "No model changes requiring migrations"
else
    error "Model changes detected without migrations"
    echo "   Run: python manage.py makemigrations"
    echo "   Changes:"
    echo "$MIGRATION_CHECK" | grep -A10 "Migrations for" || echo "$MIGRATION_CHECK"
fi

echo ""
echo "5. Running Django system checks..."
SYS_CHECK_OUTPUT=$($PYTHON_CMD manage.py check 2>&1) || true
if echo "$SYS_CHECK_OUTPUT" | grep -q "System check identified no issues"; then
    success "Django system checks passed"
else
    warning "Django issues found:"
    echo "$SYS_CHECK_OUTPUT" | head -20
fi

echo ""
echo "6. Checking database connection..."
if $PYTHON_CMD manage.py showmigrations > /dev/null 2>&1; then
    success "Database connection OK"
else
    error "Cannot connect to database"
    echo "   Make sure DATABASE_URL is set"
fi

echo ""
echo "7. Verifying static files can be collected..."
if $PYTHON_CMD manage.py collectstatic --dry-run --no-input > /dev/null 2>&1; then
    success "Static files OK"
else
    warning "Static files collection may have issues"
fi

echo ""
echo "================================"
echo "BUILD VALIDATION SUMMARY"
echo "================================"

if [ $ERRORS -eq 0 ]; then
    success "ALL CHECKS PASSED"
    echo "Proceeding with deployment..."
    exit 0
else
    error "$ERRORS error(s) found"
    echo ""
    echo "================================"
    echo "DEPLOYMENT BLOCKED"
    echo "================================"
    echo "Fix the errors above before deploying."
    echo "Common fixes:"
    echo "  - python manage.py makemigrations"
    echo "  - Fix syntax errors in Python files"
    echo "  - Check DATABASE_URL environment variable"
    exit 1
fi