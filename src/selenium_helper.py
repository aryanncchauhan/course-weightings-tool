from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import time

def fetch_course_weightings(course_code, year, term, chrome_driver_path="C:/Program Files (x86)/chromedriver.exe"):
    # Error handling for input
    valid_years = ["2023", "2024"]
    valid_terms = ["1", "2", "3"]
    if year not in valid_years or term not in valid_terms:
        raise ValueError("Invalid year or term provided")

    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--silent") 
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Initialize WebDriver
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to the desired URL
        driver.get("https://www.unsw.edu.au/course-outlines")

        # Search course code
        search = driver.find_element(By.ID, "degree-search-input")
        search.send_keys(course_code)
        search.send_keys(Keys.RETURN)

        # Select year
        select_year = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@role="combobox" and @aria-expanded="false" and @aria-haspopup="listbox" and @aria-controls="dropdown-year-body" and @aria-labelledby="dropdown-year"]'))
        )
        select_year.click()

        if year == "2024":
            selected_year = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dropdown-year-0"))
            )
        else:
            selected_year = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dropdown-year-1"))
            )
        selected_year.click()

        # Select term
        select_term = driver.find_element(By.XPATH, '//button[@role="combobox" and @aria-expanded="false" and @aria-haspopup="listbox" and @aria-controls="dropdown-term-body" and @aria-labelledby="dropdown-term"]')
        select_term.click()

        if term == "1":
            selected_term = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dropdown-term-9"))
            )
        elif term == "2":
            selected_term = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dropdown-term-10"))
            )
        else:
            selected_term = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dropdown-term-11"))
            )
        selected_term.click()

        time.sleep(3)
        
        # Analyse search results
        try:
            tables_results = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "global-tables__results"))
            )
            
            # Open relevant course outline
            button = tables_results.find_element(By.CSS_SELECTOR, 'a')
            button.click()
        except TimeoutException:
            raise RuntimeError(f"No course outline found for {course_code.upper()} {year} Term {term}")

        # Open Assessments tab
        assessments_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-click_name="Assessments"]'))
        )
        assessments_button.click()

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
