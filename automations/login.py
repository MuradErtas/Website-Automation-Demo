"""
Login automation module.
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

def login():
    """Automates login to The Internet website."""
    cfg = config.LOGIN_CONFIG
    driver = webdriver.Chrome()
    result = {
        "success": False,
        "current_url": "",
        "timestamp": "",
        "screenshot": "",
        "html": ""
    }
    
    try:
        logger.info(f"Navigating to {cfg['url']}")
        driver.get(cfg['url'])
        
        wait = WebDriverWait(driver, cfg['timeout'])
        username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, cfg['username_selector'])))
        password_field = driver.find_element(By.CSS_SELECTOR, cfg['password_selector'])
        login_button = driver.find_element(By.CSS_SELECTOR, cfg['submit_selector'])
        
        logger.info("Entering credentials")
        username_field.send_keys(cfg['username'])
        password_field.send_keys(cfg['password'])
        
        logger.info("Clicking login button")
        login_button.click()
        
        wait.until(lambda d: d.current_url != cfg['url'])
        current_url = driver.current_url
        
        result["current_url"] = current_url
        result["timestamp"] = get_timestamp()
        
        if cfg['success_url_contains'] in current_url:
            logger.info("Login successful - redirected to secure area")
            result["success"] = True
            screenshot_path = save_screenshot(driver, get_timestamp_filename("login_success", "png"))
            result["screenshot"] = screenshot_path
        else:
            logger.error("Login failed - incorrect credentials or error occurred")
            try:
                error_element = driver.find_element(By.CSS_SELECTOR, cfg['error_message_selector'])
                logger.error(f"Error message: {error_element.text}")
            except:
                logger.error("Could not retrieve error message")
            screenshot_path = save_screenshot(driver, get_timestamp_filename("login_failure", "png"))
            html_path = save_html(driver, get_timestamp_filename("login_failure", "html"))
            result["screenshot"] = screenshot_path
            result["html"] = html_path
        
    except TimeoutException:
        logger.error("Login failed: timeout waiting for page elements")
        result["current_url"] = driver.current_url if driver else ""
        result["timestamp"] = get_timestamp()
        screenshot_path = save_screenshot(driver, get_timestamp_filename("login_timeout", "png"))
        html_path = save_html(driver, get_timestamp_filename("login_timeout", "html"))
        result["screenshot"] = screenshot_path
        result["html"] = html_path
    except Exception as e:
        logger.error(f"Login failed: {e}")
        result["current_url"] = driver.current_url if driver else ""
        result["timestamp"] = get_timestamp()
        if driver:
            screenshot_path = save_screenshot(driver, get_timestamp_filename("login_error", "png"))
            html_path = save_html(driver, get_timestamp_filename("login_error", "html"))
            result["screenshot"] = screenshot_path
            result["html"] = html_path
    finally:
        driver.quit()
        logger.info("Browser closed")
    
    return result

