from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

# Function to set up the Chrome driver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless
    chrome_options.add_argument("--no-sandbox")  # Required for some environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Reduce resource usage

    # Use the ChromeDriver provided by Railway
    driver_path = "/usr/bin/chromedriver"
    driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
    return driver
