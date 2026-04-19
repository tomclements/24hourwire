# Testing 24HourWire with Playwright

This directory contains end-to-end browser tests using Playwright.

## Installation

```bash
# Install Playwright
pip install pytest-playwright

# Install browsers
playwright install
```

## Running Tests

```bash
# Run all tests (headless mode)
pytest

# Run with browser UI visible
pytest --headed

# Run on specific browser
pytest --browser=chromium
pytest --browser=firefox
pytest --browser=webkit

# Run with trace viewer (for debugging)
pytest --tracing=on
```

## Test Files

- `test_different_angle.py` - Tests the Different Angle feature
- `test_home_page.py` - Tests basic home page functionality
- `test_navigation.py` - Tests navigation and category switching

## Debugging Failed Tests

If a test fails, Playwright generates:
- Screenshots in `test-results/`
- Trace files that can be viewed with: `playwright show-trace test-results/<trace-name>.zip`

## Writing New Tests

Use the test generator to create tests by recording your actions:

```bash
playwright codegen https://your-site-url.com
```
