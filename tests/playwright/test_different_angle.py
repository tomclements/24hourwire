"""
Playwright tests for the Different Angle feature.

Run with: pytest tests/playwright/test_different_angle.py --headed
"""

import re
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def base_url():
    """Base URL for testing - change to your production URL."""
    return "https://two4hourwire.onrender.com"  # Production URL


class TestDifferentAngle:
    """Tests for the Different Angle modal functionality."""
    
    def test_different_angle_modal_opens(self, page: Page, base_url: str):
        """Test that clicking Different Angle opens the modal."""
        page.goto(base_url)
        
        # Wait for page to load
        page.wait_for_selector(".story-card", timeout=10000)
        
        # Click the first "Different Angle" button
        first_button = page.locator("button:has-text('Different Angle')").first
        expect(first_button).to_be_visible()
        
        # Get the story title for verification
        story_title = page.locator(".story-card").first.locator("h3").text_content()
        
        # Click the button
        first_button.click()
        
        # Verify modal opens
        modal = page.locator("#different-angle-modal")
        expect(modal).to_be_visible()
        
        # Verify modal shows correct story title
        modal_title = page.locator("#different-angle-original-title")
        expect(modal_title).to_contain_text(story_title[:30])  # First 30 chars
        
    def test_different_angle_shows_loading(self, page: Page, base_url: str):
        """Test that loading indicator appears while fetching."""
        page.goto(base_url)
        page.wait_for_selector(".story-card", timeout=10000)
        
        # Click Different Angle
        page.locator("button:has-text('Different Angle')").first.click()
        
        # Verify loading is visible
        loading = page.locator("#different-angle-loading")
        expect(loading).to_be_visible()
        
        # Wait for loading to disappear (or timeout)
        try:
            loading.wait_for(state="hidden", timeout=5000)
        except:
            pass  # Loading might still be visible if no related stories
        
    def test_different_angle_switching_stories(self, page: Page, base_url: str):
        """Test that clicking different stories updates the modal correctly."""
        page.goto(base_url)
        page.wait_for_selector(".story-card", timeout=10000)
        
        # Get first two story titles
        stories = page.locator(".story-card").all()
        if len(stories) < 2:
            pytest.skip("Need at least 2 stories to test switching")
        
        story_a_title = stories[0].locator("h3").text_content()
        story_b_title = stories[1].locator("h3").text_content()
        
        # Click Story A's Different Angle
        stories[0].locator("button:has-text('Different Angle')").click()
        
        # Verify Story A is shown
        modal_title = page.locator("#different-angle-original-title")
        expect(modal_title).to_contain_text(story_a_title[:30])
        
        # Wait for fetch to complete
        page.wait_for_timeout(2000)
        
        # Click Story B's Different Angle
        stories[1].locator("button:has-text('Different Angle')").click()
        
        # Verify Story B is now shown
        expect(modal_title).to_contain_text(story_b_title[:30])
        
    def test_different_angle_modal_closes(self, page: Page, base_url: str):
        """Test that modal can be closed."""
        page.goto(base_url)
        page.wait_for_selector(".story-card", timeout=10000)
        
        # Open modal
        page.locator("button:has-text('Different Angle')").first.click()
        
        # Verify modal is visible
        modal = page.locator("#different-angle-modal")
        expect(modal).to_have_class(re.compile("active"))
        
        # Click close button
        page.locator(".close-modal").click()
        
        # Verify modal is hidden
        expect(modal).not_to_have_class(re.compile("active"))
        
    def test_different_angle_click_outside_closes(self, page: Page, base_url: str):
        """Test that clicking outside modal closes it."""
        page.goto(base_url)
        page.wait_for_selector(".story-card", timeout=10000)
        
        # Open modal
        page.locator("button:has-text('Different Angle')").first.click()
        
        modal = page.locator("#different-angle-modal")
        expect(modal).to_be_visible()
        
        # Click outside (on the modal backdrop)
        modal.click(position={"x": 10, "y": 10})
        
        # Verify modal closes
        expect(modal).not_to_be_visible()
        
    def test_different_angle_related_stories_format(self, page: Page, base_url: str):
        """Test that related stories are displayed with correct format."""
        page.goto(base_url)
        page.wait_for_selector(".story-card", timeout=10000)
        
        # Click Different Angle
        page.locator("button:has-text('Different Angle')").first.click()
        
        # Wait for fetch
        page.wait_for_timeout(3000)
        
        # Check if any related stories appeared
        related_items = page.locator(".different-angle-item")
        
        if related_items.count() > 0:
            # Verify first item has required elements
            first_item = related_items.first
            expect(first_item.locator("a")).to_be_visible()
            expect(first_item.locator(".source-tag")).to_be_visible()
            expect(first_item.locator(".bias-badge")).to_be_visible()


class TestHomePage:
    """Basic tests for home page functionality."""
    
    def test_home_page_loads(self, page: Page, base_url: str):
        """Test that home page loads successfully."""
        page.goto(base_url)
        
        # Check page title
        expect(page).to_have_title(re.compile("24HourWire"))
        
        # Check that stories are loaded
        stories = page.locator(".story-card")
        expect(stories.first).to_be_visible(timeout=10000)
        
    def test_category_tabs_switch(self, page: Page, base_url: str):
        """Test that category tabs switch content."""
        page.goto(base_url)
        page.wait_for_selector(".story-card", timeout=10000)
        
        # Find all category tabs
        tabs = page.locator(".tab").all()
        if len(tabs) < 2:
            pytest.skip("Need at least 2 tabs to test switching")
        
        # Click second tab
        tabs[1].click()
        
        # Verify tab becomes active
        expect(tabs[1]).to_have_class(re.compile("active"))
        
    def test_language_switcher(self, page: Page, base_url: str):
        """Test language switching."""
        page.goto(base_url)
        page.wait_for_selector(".story-card", timeout=10000)
        
        # Find language select
        lang_select = page.locator("select[name='lang']")
        
        if lang_select.count() > 0:
            # Switch to Spanish
            lang_select.select_option("es")
            
            # Wait for page to reload
            page.wait_for_load_state("networkidle")
            
            # Verify URL changed
            expect(page).to_have_url(re.compile("lang=es"))


def test_console_errors(page: Page, base_url: str):
    """Test that no JavaScript errors appear in console."""
    errors = []
    
    def handle_console(msg):
        if msg.type == "error":
            errors.append(msg.text)
    
    page.on("console", handle_console)
    
    page.goto(base_url)
    page.wait_for_selector(".story-card", timeout=10000)
    
    # Click Different Angle to trigger JS
    page.locator("button:has-text('Different Angle')").first.click()
    page.wait_for_timeout(2000)
    
    # Check for specific errors we want to avoid
    critical_errors = [e for e in errors if "Cannot read properties of null" in e or "undefined" in e.lower()]
    
    assert len(critical_errors) == 0, f"Critical JS errors found: {critical_errors}"
