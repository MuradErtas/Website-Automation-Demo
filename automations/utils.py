"""
Shared utility functions for automations.
"""
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def save_screenshot(driver, filename):
    """Save screenshot to artifacts/screenshots directory."""
    screenshot_dir = Path("artifacts/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    filepath = screenshot_dir / filename
    driver.save_screenshot(str(filepath))
    return str(filepath)

def save_html(driver, filename):
    """Save page HTML to artifacts/html directory."""
    html_dir = Path("artifacts/html")
    html_dir.mkdir(parents=True, exist_ok=True)
    filepath = html_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    return str(filepath)

def get_timestamp():
    """Get formatted timestamp string."""
    return datetime.now().isoformat()

def get_timestamp_filename(prefix, extension):
    """Get filename with timestamp."""
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"

