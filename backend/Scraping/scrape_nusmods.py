import os, json, requests, re, PyPDF2

"""
TODO: Automate downloading of course info pdf
"""


def get_NUS_course_info(course_code):
    """
    API Example:
    GET https://api.nusmods.com/v2/2023-2024/modules/CS1231.json
    """

    url = f"https://api.nusmods.com/v2/2023-2024/modules/{course_code}.json"
    res = requests.get(url)
    data = json.loads(res.text)
    return {"course_code": course_code,
            "course_name": data["title"],
            "course_description": data["description"],
            'prereqTree': data.get('prereqTree', "")}


def scrape_nus(school, major, link):
    # Regex pattern: 2 or 3 letters, then 4 numbers, then 1 optional letter. Followed by space and then other words
    NUS_pattern = "([a-zA-Z]{2,3}[0-9]{4}[a-zA-Z]?) +\w+"

    output = []
    print(school, major)
    content = ""

    if f"{school}_{major}.pdf" in os.listdir("./data/majors_info"):  # Major details is in pdf
        for page in PyPDF2.PdfReader(open(f"./data/majors_info/{school}_{major}.pdf", "rb")).pages:
            content += page.extract_text()
        content = content.replace(" ", " ")   # replace weird space character
    else:  # Major details is on the website
        content = requests.get(link).text

    course_codes = dict()   # Ordered and prevents duplicates
    for match in re.finditer(NUS_pattern, content):
        course_codes[match.group(1)] = ""
    for course_code in course_codes:
        print(course_code)
        try:
            course_info = get_NUS_course_info(course_code)
            output.append([school, major] + list(course_info.values()))
        except Exception as e:
            print(f"Error getting course information for {course_code} due to {e}")
            continue

    return output