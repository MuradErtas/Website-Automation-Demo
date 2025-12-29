"""
Dynamic content loading automation - handle JS-loaded elements with waits.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import time
import config
from automations.utils import save_screenshot, save_html, get_timestamp, get_timestamp_filename

logger = logging.getLogger(__name__)

def wait_with_retry(driver, selector, max_retries=3, retry_delay=1):
    """Wait for element with retry logic."""
    for attempt in range(max_retries):
        try:
            wait = WebDriverWait(driver, config.DYNAMIC_CONFIG['timeout'])
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return element
        except TimeoutException:
            if attempt < max_retries - 1:
                logger.info(f"Retry {attempt + 1}/{max_retries} for {selector}")
                time.sleep(retry_delay)
            else:
                raise

def dynamic_loading():
    """Handle dynamically loaded content with explicit waits."""
    cfg = config.DYNAMIC_CONFIG
    driver = webdriver.Chrome()
    
    result = {
        "success": False,
        "element_found": False,
        "element_text": "",
        "timestamp": "",
        "screenshot": ""
    }
    
    try:
        logger.info(f"Navigating to {cfg['url']}")
        driver.get(cfg['url'])
        
        # Click trigger button
        wait = WebDriverWait(driver, cfg['timeout'])
        trigger_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cfg['trigger_selector'])))
        logger.info("Clicking trigger button to load dynamic content")
        trigger_button.click()
        
        # Wait for dynamic element with retry
        logger.info("Waiting for dynamic element to appear")
        dynamic_element = wait_with_retry(driver, cfg['dynamic_element_selector'])
        
        element_text = dynamic_element.text
        result["element_found"] = True
        result["element_text"] = element_text
        result["timestamp"] = get_timestamp()
        result["success"] = True
        
        logger.info(f"Dynamic element found: {element_text}")
        screenshot_path = save_screenshot(driver, get_timestamp_filename("dynamic_success", "png"))
        result["screenshot"] = screenshot_path
        
    except TimeoutException:
        logger.error("Dynamic loading failed: timeout waiting for element")
        result["timestamp"] = get_timestamp()
        screenshot_path = save_screenshot(driver, get_timestamp_filename("dynamic_failure", "png"))
        html_path = save_html(driver, get_timestamp_filename("dynamic_failure", "html"))
        result["screenshot"] = screenshot_path
    except Exception as e:
        logger.error(f"Dynamic loading failed: {e}")
        result["timestamp"] = get_timestamp()
        if driver:
            screenshot_path = save_screenshot(driver, get_timestamp_filename("dynamic_error", "png"))
            result["screenshot"] = screenshot_path
    finally:
        driver.quit()
        logger.info("Browser closed")
    
    return result

