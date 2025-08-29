from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

import sys
import time

# Dismiss the cookie banner before doing anything else
def dismiss_cookies(driver):
    try:
        # Common OneTrust accept button id
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        try:
            btn.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", btn)
        # small wait for banner to disappear
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.ID, "onetrust-banner-sdk"))
        )
    except Exception:
        # If not present, ignore
        pass

# Safe click helper that scrolls + falls back to JS if intercepted 
def safe_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element))
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)

def fetch_course_weightings(course_code, year, term):
    # Error handling for input
    valid_years = ["2023", "2024", "2025"]
    valid_terms = ["1", "2", "3"]
    if year not in valid_years or term not in valid_terms:
        raise ValueError("Invalid year or term provided")

    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")  
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the desired URL
        driver.get("https://www.unsw.edu.au/course-outlines")
        
        dismiss_cookies(driver)

        # Search course code
        search = driver.find_element(By.ID, "degree-search-input")
        search.send_keys(course_code)
        search.send_keys(Keys.RETURN)

        # Select year
        select_year = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@role="combobox" and @aria-expanded="false" and @aria-haspopup="listbox" and @aria-controls="dropdown-year-body" and @aria-labelledby="dropdown-year"]'))
        )
        safe_click(driver, select_year)

        if year == "2025":
            selected_year = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dropdown-year-0"))
            )
        elif year == "2024":
            selected_year = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dropdown-year-1"))
            )
        else:
            selected_year = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dropdown-year-2"))
            )
        safe_click(driver, selected_year) 

        # Select term
        select_term = driver.find_element(By.XPATH, '//button[@role="combobox" and @aria-expanded="false" and @aria-haspopup="listbox" and @aria-controls="dropdown-term-body" and @aria-labelledby="dropdown-term"]')
        safe_click(driver, select_term)

        if term == "1":
            selected_term = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dropdown-term-10"))
            )
        elif term == "2":
            selected_term = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dropdown-term-11"))
            )
        else:
            selected_term = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dropdown-term-12"))
            )
        safe_click(driver, selected_term)

        time.sleep(3)
        
        # Analyse search results
        try:
            tables_results = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "global-tables__results"))
            )
            
            # Open relevant course outline
            button = tables_results.find_element(By.CSS_SELECTOR, 'a')
            safe_click(driver, button)
        except TimeoutException:
            raise RuntimeError(f"No course outline found for {course_code.upper()} {year} Term {term}")

        # Open Assessments tab
        assessments_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-click_name="Assessments"]'))
        )
        safe_click(driver, assessments_button) 

        # Handle assessment items
        course_outline = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-component_id="text-1785249165"]'))
        )
        table_entries = course_outline.find_elements(By.CSS_SELECTOR, 'tr')
        weightings = []
        for table_entry in table_entries:
            cells = table_entry.find_elements(By.CSS_SELECTOR, 'td')
            if len(cells) > 1:
                assessment_name = cells[0].text.split("\n")[0]
                weighting = cells[1].text
                weightings.append((assessment_name, weighting))

        return weightings

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return []
    
    finally:
        driver.quit()
