from selenium import webdriver
from selenium.webdriver.common.by import By
import time, string
import csv
import re


def wait_for_page_to_load(driver):
    # Funny SMU page shows a loading gif when the page is not ready
    # When ready, the style attribute becomes "display: none" from "display: block;"
    while "display: block;" in driver.find_element(By.ID, "WAIT_win0").get_attribute("style"):
        time.sleep(0.2)
    time.sleep(0.2)


data = [["course_code", "course_name", "course_description"]]

driver = webdriver.Chrome()
driver.get("https://publiceservices.smu.edu.sg/psc/ps/EMPLOYEE/HRMS/c/SIS_CR.SIS_CLASS_SEARCH.GBL?&")  # Load cookies
driver.get("https://publiceservices.smu.edu.sg/psc/ps/EMPLOYEE/HRMS/c/SIS_CR.SIS_CLASS_SEARCH.GBL?&")  # Works properly only after the second try
for c in string.ascii_uppercase[:]:
    print(f"Scraping page {c} .....")
    driver.execute_script(f"submitAction_win0(document.win0,'SSR_CLSRCH_WRK2_SSR_ALPHANUM_{c}');")
    wait_for_page_to_load(driver)
    driver.find_element(By.ID, "DERIVED_CRSECAT_SSR_CRSECAT_DISP").click()
    wait_for_page_to_load(driver)
    i = 0
    while len(driver.find_elements(By.ID, f"DERIVED_CLSRCH_COURSE_TITLE_LONG${i}"))>0:
        try:
            # Click into the i-th course on the catalog page
            driver.execute_script(f"submitAction_win0(document.win0,'DERIVED_CLSRCH_COURSE_TITLE_LONG${i}');")
            wait_for_page_to_load(driver)

            course_title = driver.find_element(By.ID, "DERIVED_CRSECAT_DESCR200").text
            if course_title[:4] == "COR-":  # If course title is "COR-XX 1234 - XXXX", split at second dash
                split_at = course_title[4:].index("-") + 4
            else:
                split_at = course_title.index("-")
            course_code, course_name = course_title[:split_at], course_title[split_at+1:]
            course_code = course_code.replace(".", " ")  # Remove dot in course code
            while course_code.count(" ") > 0:
                course_code = course_code.replace(" ", "")  # Remove spaces
            course_name = course_name.strip()
            print(course_code, course_name)

            course_description = driver.find_element(By.ID, "SSR_CRSE_OFF_VW_DESCRLONG$0").text
            course_description = re.sub(r'[^\x00-\x7F]+', ' ', course_description)  # Remove non-ASCII characters



            data.append([course_code, course_name, course_description])
            i += 1

        except Exception as e:
            print("Error getting course at", c, i)
            print(e)
            i += 1
            pass

        try:
            # Return to catalog page
            driver.execute_script("submitAction_win0(document.win0,'DERIVED_SAA_CRS_RETURN_PB$163$');")
            wait_for_page_to_load(driver)
        except Exception as e:
            print("Error returning to catalog at", c, i)
            print(e)
            pass



print("finished scraping, saving data...")

with open("./data/smu_courses_all.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)