import csv, re
from selenium import webdriver
import time

def scrape_smu(school, major, link):
    print(school, major)

    # Run scrape_smu_all_courses.py to generate ./data/smu_courses_all.csv
    with open("./data/smu_courses_all.csv", "r") as f:
        reader = csv.reader(f)
        all_courses_info = {row[0]:row for row in reader}
    all_courses_info.pop("course_code")  # Remove header column

    # capital letters (may have dash) followed by 3 or 4 digits, then continues with non-digit characters
    SMU_pattern = "([A-Z]+-?[A-Z]+ ?[0-9]{3,4})[^0-9]"
    course_codes = dict()   # Ordered and prevents duplicates

    if major == "Information Systems (Business Analytics)":
        # IS-BZA website is too complicated to scrape. Not worth the effort.
        ISBZA_courses = ["IS114", "IS210", "IS214", "IS212", "IS215", "IS111", "IS112", "IS211", "IS113", "IS216",
                         "IS213", "IS217", "IS461", "IS454", "IS459", "IS424", "IS453", "IS415", "CS420", "CS421",
                         "IS460", "IS446", "IS455", "IS434", "IS450", "IS428"]
        for course in ISBZA_courses:
            course_codes[course] = ""
    else:
        # SMU sites disallow requests.get().
        driver = webdriver.Chrome()
        driver.get(link)
        time.sleep(5)   # Load the page
        html = driver.page_source
        for match in re.finditer(SMU_pattern, html):  # Get courses
            course_codes[match.group(1)] = ""

    output = []
    for course_code in course_codes:
        if course_code in all_courses_info:
            print(course_code)
            output.append([school, major] + all_courses_info[course_code] + [""])  # Not scraping prereqs
        else:
            print(f"Error getting info for {course_code}")

    return output


if __name__ == '__main__':
    # Testing
    (scrape_smu("SMU","Information Systems (Business Analytics)", "https://economics.smu.edu.sg/bachelor-science-economics/curriculum/2nd-major-data-science-and-analytics"))

