import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from datetime import datetime
from bs4 import BeautifulSoup
import json

def initialize_driver(headless=True):
    """Initialize the Chrome WebDriver with options."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def main(driver,config=None):
    """Scrape documents from the given URL, handling pagination and retries as necessary, saving metadata after each page."""
    
    driver.get(config["url"])

    time.sleep(5)
   

if __name__ == "__main__":
    config = {"url": "https://hbr.org",                            
              "headless": False} 
    driver = initialize_driver(config["headless"])
    main(driver=driver, config=config)
