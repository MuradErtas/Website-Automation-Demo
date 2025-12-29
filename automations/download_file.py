"""
Download file automation - download a file and verify.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import time
from pathlib import Path
import config
from automations.utils import save_screenshot, save_html, get_timestamp, get_timestamp_filename

logger = logging.getLogger(__name__)

def download_file():
    """Download a file and verify it exists with size > 0."""
    download_dir = Path("artifacts/downloads")
    download_dir.mkdir(parents=True, exist_ok=True)
    
    cfg = config.DOWNLOAD_CONFIG
    
    # Set download preferences
    prefs = {"download.default_directory": str(download_dir.absolute())}
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    
    result = {
        "success": False,
        "file_path": "",
        "file_size": 0,
        "timestamp": "",
        "screenshot": ""
    }
    
    try:
        # Navigate to download page
        logger.info(f"Navigating to {cfg['url']}")
        driver.get(cfg['url'])
        
        wait = WebDriverWait(driver, cfg['timeout'])
        download_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, cfg['download_link_selector'])))
        
        logger.info("Clicking download link")
        download_link.click()
        
        # Wait for download to complete
        logger.info("Waiting for download to complete")
        time.sleep(3)
        
        # Verify file exists and has size > 0
        downloaded_files = list(download_dir.glob(cfg['expected_filename']))
        if downloaded_files:
            file_path = downloaded_files[0]
            file_size = file_path.stat().st_size
            result["file_path"] = str(file_path)
            result["file_size"] = file_size
            result["timestamp"] = get_timestamp()
            
            if file_size > 0:
                logger.info(f"Download successful: {file_path} ({file_size} bytes)")
                result["success"] = True
                screenshot_path = save_screenshot(driver, get_timestamp_filename("download_success", "png"))
                result["screenshot"] = screenshot_path
            else:
                logger.error("Downloaded file is empty")
                screenshot_path = save_screenshot(driver, get_timestamp_filename("download_failure", "png"))
                result["screenshot"] = screenshot_path
        else:
            logger.error("Downloaded file not found")
            screenshot_path = save_screenshot(driver, get_timestamp_filename("download_failure", "png"))
            result["screenshot"] = screenshot_path
            result["timestamp"] = get_timestamp()
            
    except TimeoutException:
        logger.error("Download failed: timeout")
        result["timestamp"] = get_timestamp()
        screenshot_path = save_screenshot(driver, get_timestamp_filename("download_timeout", "png"))
        html_path = save_html(driver, get_timestamp_filename("download_timeout", "html"))
        result["screenshot"] = screenshot_path
    except Exception as e:
        logger.error(f"Download failed: {e}")
        result["timestamp"] = get_timestamp()
        if driver:
            screenshot_path = save_screenshot(driver, get_timestamp_filename("download_error", "png"))
            result["screenshot"] = screenshot_path
    finally:
        driver.quit()
        logger.info("Browser closed")
    
    return result

