import os, json, requests, re, csv

"""
TODO: Regex prereq, parse prereq
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

    for match in re.finditer(NTU_pattern, content):
        course_code, course_name, course_info = match.group(1), match.group(2), match.group(4)
        print(course_code, course_name)
        for prereq_match in re.finditer(prereq_pattern, match.group(3)):
            print(prereq_match.group(1))




output = [["School", "Major", "Course_Code", "Course_Name", "Course_Description", "Prereq_Tree"]]

major_links = [row for row in csv.reader(open("./data/majors_links.csv", 'r'))]

get_NTU_course_info("DSAI", 2)
