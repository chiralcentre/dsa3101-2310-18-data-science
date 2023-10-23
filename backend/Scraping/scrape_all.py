import csv
from scrape_nusmods import *
from scrape_ntu import *

output = [["School", "Major", "Course_Code", "Course_Name", "Course_Description", "Prereq"]]

major_links = [row for row in csv.reader(open("./data/majors_links.csv", 'r'))]

for school, major, link in major_links:
    if school == "NUS":
        output += scrape_nus(school, major, link)
    elif school == "NTU":
        output += scrape_ntu(school, major, link)


with open("./data/module_details.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output)