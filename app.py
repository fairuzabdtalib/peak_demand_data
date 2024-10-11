from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Chrome options for headless mode
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')

# Path to ChromeDriver
chrome_service = Service('/usr/bin/chromedriver')

# Initialize Chrome WebDriver with options
driver = webdriver.Chrome(service=chrome_service, options=options)

# Open the page
url = "https://www.gso.org.my/SystemData/SystemDemand.aspx"
driver.get(url)

try:
    # Optional: Add a delay to allow content to load
    time.sleep(5)

    # Wait until the table with class 'table' is present
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table")))

    # Get the page source after JavaScript execution
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Locate the table
    table = soup.find('table', class_='table')

    if table is None:
        print("Table with the specified class not found.")
    else:
        # Locate all rows within the table body
        rows = table.find('tbody').find_all('tr')

        # Prepare lists to store extracted data
        date_time = []
        mw_values = []

        # Iterate over each row and extract data
        for row in rows:
            date_time_value = row.find_all('td')[0].text.strip()
            mw_value = row.find('td', class_='mw').text.strip()
            date_time.append(date_time_value)
            mw_values.append(mw_value)

        # Create a DataFrame
        data = pd.DataFrame({'Date Time': date_time, 'MW': mw_values})
        data['MW'] = pd.to_numeric(data['MW'])
        
        # Display the DataFrame
        print(data)

finally:
    driver.quit()
