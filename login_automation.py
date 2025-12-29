"""
Web automation demo for logging into The Internet website.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Login credentials
USERNAME = "tomsmith"
PASSWORD = "SuperSecretPassword!"
LOGIN_URL = "https://the-internet.herokuapp.com/login"

def login():
    """Automates login to The Internet website."""
    # Initialize Chrome driver
    driver = webdriver.Chrome()
    
    try:
        # Navigate to login page
        print(f"Opening {LOGIN_URL}...")
        driver.get(LOGIN_URL)
        
        # Wait for page to load and find elements
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        # Enter credentials
        print("Entering credentials...")
        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        
        # Click login button
        print("Clicking login button...")
        login_button.click()
        
        # Wait for redirect and check result
        time.sleep(2)  # Brief wait for page transition
        
        # Check if login was successful (look for success message or secure area)
        current_url = driver.current_url
        if "secure" in current_url.lower():
            print("✓ Login successful! Redirected to secure area.")
        else:
            # Check for error message
            try:
                error_message = driver.find_element(By.ID, "flash").text
                print(f"✗ Login failed: {error_message}")
            except:
                print("✗ Login status unclear.")
        
        # Keep browser open for a few seconds to see result
        print("Keeping browser open for 5 seconds...")
        time.sleep(5)
        
    except TimeoutException:
        print("✗ Timeout: Page elements not found.")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        # Close browser
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    login()

