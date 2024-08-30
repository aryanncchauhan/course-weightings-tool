import sys
from selenium_helper import fetch_course_weightings

# Get input from user
course_code = input("Please enter course code: ")
year = input("Please enter year offered: ")
term = input("Please enter term offered: ")

# Fetch course weightings
try:
    weightings = fetch_course_weightings(course_code, year, term)
    if weightings:
        print("")
        print(f"{course_code.upper()} {year} Term {term}: ")
        for assessment_name, weighting in weightings:
            print(f"- \"{assessment_name}\" has a weighting of {weighting}")
        print("")
except RuntimeError as re:
    print(re, file=sys.stderr)
except ValueError as ve:
    print(f"Input error: {ve}", file=sys.stderr)
