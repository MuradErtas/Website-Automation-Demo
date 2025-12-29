"""
Form fill and submit automation.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import config
from automations.utils import save_screenshot, save_html, get_timestamp, get_timestamp_filename

logger = logging.getLogger(__name__)

def fill_form():
    """Fill form fields and submit."""
    cfg = config.FORM_CONFIG
    driver = webdriver.Chrome()
    
    result = {
        "success": False,
        "current_url": "",
        "timestamp": "",
        "screenshot": ""
    }
    
    try:
        logger.info(f"Navigating to {cfg['url']}")
        driver.get(cfg['url'])
        
        wait = WebDriverWait(driver, cfg['timeout'])
        
        # Fill all form fields
        logger.info("Filling form fields")
        for field_config in cfg['fields']:
            field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, field_config['selector'])))
            field.clear()
            field.send_keys(field_config['value'])
            logger.info(f"Filled {field_config['name']}")
        
        # Submit form
        submit_button = driver.find_element(By.CSS_SELECTOR, cfg['submit_selector'])
        logger.info("Submitting form")
        submit_button.click()
        
        # Wait for success indicator
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, cfg['success_selector'])))
        current_url = driver.current_url
        
        result["current_url"] = current_url
        result["timestamp"] = get_timestamp()
        result["success"] = True
        
        logger.info("Form submitted successfully")
        screenshot_path = save_screenshot(driver, get_timestamp_filename("form_success", "png"))
        result["screenshot"] = screenshot_path
        
    except TimeoutException:
        logger.error("Form submission failed: timeout waiting for success")
        result["current_url"] = driver.current_url if driver else ""
        result["timestamp"] = get_timestamp()
        screenshot_path = save_screenshot(driver, get_timestamp_filename("form_failure", "png"))
        html_path = save_html(driver, get_timestamp_filename("form_failure", "html"))
        result["screenshot"] = screenshot_path
    except Exception as e:
        logger.error(f"Form submission failed: {e}")
        result["current_url"] = driver.current_url if driver else ""
        result["timestamp"] = get_timestamp()
        if driver:
            screenshot_path = save_screenshot(driver, get_timestamp_filename("form_error", "png"))
            result["screenshot"] = screenshot_path
    finally:
        driver.quit()
        logger.info("Browser closed")
    
    return result

