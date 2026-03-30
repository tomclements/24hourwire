# Pre-deployment testing script for 24HourWire
# Run this before committing/pushing to catch errors locally

Write-Host "================================" -ForegroundColor Cyan
Write-Host "24HourWire Pre-Deploy Checklist"
Write-Host "================================"
Write-Host ""

$errors = 0
$warnings = 0

# 1. Check if Python is available
Write-Host "1. Checking Python..."
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}

if ($python) {
    Write-Host "✓ Python found: $($python.Source)" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found" -ForegroundColor Red
    exit 1
}

# 2. Check Django installation
Write-Host ""
Write-Host "2. Checking Django..."
try {
    $djangoVersion = & $python.Source -c "import django; print(django.__version__)" 2>$null
    if ($djangoVersion) {
        Write-Host "✓ Django $djangoVersion installed" -ForegroundColor Green
    } else {
        Write-Host "✗ Django not installed" -ForegroundColor Red
        Write-Host "   Run: pip install -r requirements.txt"
        $errors++
    }
} catch {
    Write-Host "✗ Django not installed" -ForegroundColor Red
    $errors++
}

# 3. Check for pending migrations
Write-Host ""
Write-Host "3. Checking for pending migrations..."
try {
    $migrationOutput = & $python.Source manage.py showmigrations --plan 2>&1
    $pendingMigrations = ($migrationOutput | Select-String "\[ \]" | Measure-Object).Count
    
    if ($pendingMigrations -gt 0) {
        Write-Host "⚠ $pendingMigrations pending migrations found" -ForegroundColor Yellow
        $warnings++
    } else {
        Write-Host "✓ All migrations applied" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Could not check migrations" -ForegroundColor Yellow
    $warnings++
}

# 4. Check for model changes without migrations
Write-Host ""
Write-Host "4. Checking for model changes without migrations..."
try {
    $migrationCheck = & $python.Source manage.py makemigrations --dry-run --check 2>&1
    if ($migrationCheck -match "No changes detected") {
        Write-Host "✓ No model changes requiring migrations" -ForegroundColor Green
    } else {
        Write-Host "✗ Model changes detected without migrations" -ForegroundColor Red
        Write-Host "   Run: python manage.py makemigrations"
        $errors++
    }
} catch {
    Write-Host "✗ Model changes detected without migrations" -ForegroundColor Red
    $errors++
}

# 5. Run Django system checks
Write-Host ""
Write-Host "5. Running Django system checks..."
try {
    $sysCheck = & $python.Source manage.py check 2>&1
    if ($sysCheck -match "System check identified no issues" -or $LASTEXITCODE -eq 0) {
        Write-Host "✓ Django system checks passed" -ForegroundColor Green
    } else {
        Write-Host "⚠ Django issues found:" -ForegroundColor Yellow
        $sysCheck | Select-String "WARNINGS|ERRORS" -Context 0,2
        $warnings++
    }
} catch {
    Write-Host "⚠ Could not run Django checks" -ForegroundColor Yellow
    $warnings++
}

# 6. Check for syntax errors
Write-Host ""
Write-Host "6. Checking for Python syntax errors..."
$syntaxErrors = 0
$pythonFiles = Get-ChildItem -Recurse -Filter "*.py" -Exclude "venv",".git","__pycache__"

foreach ($file in $pythonFiles) {
    try {
        $null = & $python.Source -m py_compile $file.FullName 2>&1
    } catch {
        Write-Host "✗ Syntax error in: $($file.FullName)" -ForegroundColor Red
        $syntaxErrors++
    }
}

if ($syntaxErrors -eq 0) {
    Write-Host "✓ No Python syntax errors" -ForegroundColor Green
} else {
    Write-Host "✗ $syntaxErrors Python file(s) with syntax errors" -ForegroundColor Red
    $errors += $syntaxErrors
}

# 7. Summary
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "SUMMARY"
Write-Host "================================"

if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "✓ ALL CHECKS PASSED" -ForegroundColor Green
    Write-Host "Safe to deploy!"
    exit 0
} elseif ($errors -eq 0) {
    Write-Host "⚠ $warnings warning(s) found" -ForegroundColor Yellow
    Write-Host "Review warnings, but should be safe to deploy"
    exit 0
} else {
    Write-Host "✗ $errors error(s) found" -ForegroundColor Red
    if ($warnings -gt 0) {
        Write-Host "⚠ $warnings warning(s)" -ForegroundColor Yellow
    }
    Write-Host "Fix errors before deploying!"
    exit 1
}