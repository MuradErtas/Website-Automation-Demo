"""
Paginated table scraping automation - extract data to CSV.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import csv
from pathlib import Path
import config
from automations.utils import save_screenshot, get_timestamp, get_timestamp_filename

logger = logging.getLogger(__name__)

def scrape_paginated_table():
    """Scrape paginated table and save to CSV."""
    cfg = config.SCRAPE_CONFIG
    driver = webdriver.Chrome()
    
    result = {
        "success": False,
        "rows_scraped": 0,
        "csv_path": "",
        "timestamp": "",
        "screenshot": ""
    }
    
    all_rows = []
    seen_rows = set()
    
    try:
        logger.info(f"Navigating to {cfg['url']}")
        driver.get(cfg['url'])
        
        wait = WebDriverWait(driver, cfg['timeout'])
        
        while True:
            # Wait for table to load
            table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, cfg['table_selector'])))
            rows = table.find_elements(By.CSS_SELECTOR, cfg['row_selector'])
            
            logger.info(f"Scraping {len(rows)} rows from current page")
            
            # Extract data from rows
            for row in rows:
                cells = row.find_elements(By.CSS_SELECTOR, cfg['cell_selector'])
                row_data = [cell.text.strip() for cell in cells]
                row_key = tuple(row_data)
                
                # De-duplicate
                if row_key not in seen_rows:
                    seen_rows.add(row_key)
                    all_rows.append(row_data)
            
            # Check for next page button
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, cfg['next_button_selector'])
                if "disabled" in next_button.get_attribute("class") or not next_button.is_enabled():
                    logger.info("Reached last page")
                    break
                next_button.click()
                wait.until(EC.staleness_of(table))
            except NoSuchElementException:
                logger.info("No next page button found")
                break
        
        # Write to CSV
        csv_dir = Path("artifacts/data")
        csv_dir.mkdir(parents=True, exist_ok=True)
        csv_path = csv_dir / "output.csv"
        
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if cfg.get('headers'):
                writer.writerow(cfg['headers'])
            writer.writerows(all_rows)
        
        result["success"] = True
        result["rows_scraped"] = len(all_rows)
        result["csv_path"] = str(csv_path)
        result["timestamp"] = get_timestamp()
        
        logger.info(f"Scraped {len(all_rows)} unique rows, saved to {csv_path}")
        screenshot_path = save_screenshot(driver, get_timestamp_filename("scrape_success", "png"))
        result["screenshot"] = screenshot_path
        
    except TimeoutException:
        logger.error("Scraping failed: timeout")
        result["timestamp"] = get_timestamp()
        screenshot_path = save_screenshot(driver, get_timestamp_filename("scrape_failure", "png"))
        result["screenshot"] = screenshot_path
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        result["timestamp"] = get_timestamp()
        if driver:
            screenshot_path = save_screenshot(driver, get_timestamp_filename("scrape_error", "png"))
            result["screenshot"] = screenshot_path
    finally:
        driver.quit()
        logger.info("Browser closed")
    
    return result

