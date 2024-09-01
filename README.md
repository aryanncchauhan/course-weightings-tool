# Course Weightings Tool
A tool used to retrieve assessments and their weightings for UNSW courses.

## Table of Contents
- [Motivation](#motivation)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Motivation
As a student, I often found myself needing to refer to courses' course outlines to see the different weightings of assessments. However, I was not a fan of UNSW's [Course Outline Finder](https://www.unsw.edu.au/course-outlines) and found the process tedious - especially since I was usually only concerned with assessment weightings rather than seeing the whole course outline.

To address this issue I chose to make this program which is given a course code, year, and term, and using this information scrapes the website to return the relevant weightings.

## Installation
1. Clone the repository:
```bash
git clone git@github.com:aryanncchauhan/course-weightings-tool.git
```

2. Install the Selenium library:
```bash
pip install selenium
```

3. Download [ChromeDriver](https://sites.google.com/chromium.org/driver/downloads/version-selection?authuser=0).

4. Update the ChromeDriver path in **selenium_helper.py** (if needed).

## Usage
Run the script using:
```bash
python3 main.py
```

**Course code** must be entered in the format AAAA9999: i.e. comp1511. Course code is case insensitive.

**Year** must be entered in the format YYYY. Only accepted years are 2023 and 2024.

**Term** must be 1, 2, or 3.

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software, provided that you include the original copyright notice and this license in any copies or substantial portions of the software.

For more details, please see the [LICENSE](https://choosealicense.com/licenses/mit/) file.