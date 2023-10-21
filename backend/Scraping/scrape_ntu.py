import requests, re

"""
TODO: parse prereq
"""



def get_NTU_course_info(major_code, year):
    """
    Sample request:
    POST https://wis.ntu.edu.sg/webexe/owa/AUS_SUBJ_CONT.main_display1
    acadsem: 2023_1
    r_course_yr: DSAI;;2;F
    r_subj_code: Enter Keywords or Course Code
    boption: CLoad
    acad: 2023
    semester: 1
    """

    url = "https://wis.ntu.edu.sg/webexe/owa/AUS_SUBJ_CONT.main_display1"
    post_data = {}
    post_data["acadsem"] = "2023_1"
    post_data["r_course_yr"] = f"{major_code};;{year};F"
    post_data["boption"] = "CLoad"
    post_data["acad"] = "2023"
    post_data["semester"] = "1"

    res = requests.post(url, data=post_data)
    content = res.text

    """
    Sample of 1 course information in the html
    <TABLE >
    <TR>
    <TD WIDTH="100"><B><FONT SIZE=2 COLOR=#0000FF>CC0001</FONT></B></TD>
    <TD WIDTH="500"><B><FONT SIZE=2 COLOR=#0000FF>INQUIRY & COMMUNICATION IN AN INTERDISCIPLINARY WORLD</FONT></B></TD>
    ...
    <TD><B><FONT SIZE=2 COLOR=#FF00FF>Prerequisite:</FONT></B></TD>
    <TD COLSPAN="2"><B><FONT  SIZE=2 COLOR=#FF00FF>SC1007 & SC1015 & SC2000 OR</FONT></B></TD>
    </TR>
    ...
    <TD WIDTH="650" colspan="3"><FONT SIZE=2>
    Description Description Description Description
    Description Description Description Description
    </TD>
    </TR>
    </TABLE>
    courses are separated by &nbsp;
    """

    NTU_pattern = """<TD WIDTH="100"><B><FONT SIZE=2 COLOR=#0000FF>(\w+)</FONT></B></TD>
<TD WIDTH="500"><B><FONT SIZE=2 COLOR=#0000FF>([ -~]+)</FONT></B></TD>
([ -~\n]+)
<TD WIDTH="650" colspan="3"><FONT SIZE=2>
([ -~\n]+)
</TD>
</TR>
</TABLE>"""

    prereq_pattern = '<TD COLSPAN="2"><B><FONT  SIZE=2 COLOR=#FF00FF>([^<>]+)</FONT></B></TD>'

    content = content.replace("&nbsp", chr(0))  # A non-printable char to act as separator between courses

    output = {}
    for match in re.finditer(NTU_pattern, content):
        course_code, course_name, course_description = match.group(1), match.group(2), match.group(4)
        output[course_code] = [course_code]
        output[course_code].append(course_name)
        output[course_code].append(course_description)
        output[course_code].append([])
        print(course_code, course_name)
        for prereq_match in re.finditer(prereq_pattern, match.group(3)):
            output[course_code][-1].append(prereq_match.group(1))

    return output


def scrape_ntu(school, major, link):
    print(school, major)
    output = {}
    for year in range(1,5):
        for k,v in get_NTU_course_info(link, year).items():
            output[k] = [school, major] + v
    return list(output.values())
