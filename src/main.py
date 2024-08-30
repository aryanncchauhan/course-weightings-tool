from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import time

# Get input from user
course_code = input("Please enter course code: ")
year = input("Please enter year offered: ")
term = input("Please enter term offered: ")

# Error handling for input
valid_years = ["2023", "2024"]
valid_terms = ["1", "2", "3"]
if year not in valid_years:
    print("Error: Year must be 2023 or 2024", file=sys.stderr)
    sys.exit(1)
elif term not in valid_terms:
    print("Error: Term must be 1, 2, or 3", file=sys.stderr)
    sys.exit(1)

# Allow the tab to stay open until closed
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

# Specify the path to the chromedriver executable
PATH = "C:/Program Files (x86)/chromedriver.exe"

# Create a Service object with the path to chromedriver
service = Service(executable_path=PATH)

# Initialize the WebDriver with the service object
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the desired URL
driver.get("https://www.unsw.edu.au/course-outlines")

# Search course code
search = driver.find_element(By.ID, "degree-search-input")
search.send_keys(course_code)
search.send_keys(Keys.RETURN)

# Select year
select_year = driver.find_element(By.XPATH, '//button[@role="combobox" and @aria-expanded="false" and @aria-haspopup="listbox" and @aria-controls="dropdown-year-body" and @aria-labelledby="dropdown-year"]')
driver.implicitly_wait(5)
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
driver.implicitly_wait(5)
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

# Analyse search results
try:
    tables_results = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "global-tables__results"))
    )
    
    # Open relevant course outline
    button = tables_results.find_element(By.CSS_SELECTOR, 'a')
    button.click()
except:
    print(f"No course outline found for {course_code.upper()} {year} Term {term}", file=sys.stderr)
    sys.exit(1)
    
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
for table_entry in table_entries:
    cells = table_entry.find_elements(By.CSS_SELECTOR, 'td')
    if len(cells) > 1:
        assessment_name = cells[0].text.split("\n")[0]
        weighting = cells[1].text
        print(f"\"{assessment_name}\" has a weighting of {weighting}")

driver.quit()