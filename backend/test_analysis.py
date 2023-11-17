from conftests import client
import pandas as pd

job_df = pd.read_csv("./data/job_offers_categorized.csv")

# /analysis/similar_courses endpoint
def test_similar_courses_missing_params(client):
    response = client.get("/analysis/similar_courses", query_string = {"university": "NUS", "major": "Data Science and Analytics"})
    assert response.status_code == 400
    assert response.text == "Please input all course details - school, major, course_code, course_name"

def test_similar_courses_all_params(client):
    response = client.get("/analysis/similar_courses", query_string = {"university": "NUS", "major": "Data Science and Analytics", "course_code": "CS2040", "course_name": "Data Structures and Algorithms"})
    assert response.status_code == 200

# /analysis/similar_courses_from_job_desc endpoint
def test_similar_courses_from_job_desc(client):
    response = client.get("/analysis/similar_courses_from_job_desc", query_string = {"description": job_df["job_desc"].iloc[0]})
    assert response.status_code == 200

# /analysis/similar_courses_from_job_type endpoint
def test_similar_courses_from_job_type_missing_params(client):
    response = client.get("/analysis/similar_courses_from_job_type")
    assert response.status_code == 400
    assert response.text == "Please input job_type"

def test_similar_courses_from_job_type_all_params(client):
    response = client.get("/analysis/similar_courses_from_job_type", query_string = {"job_type": "Data Analyst"})
    assert response.status_code == 200

# /analysis/compare_programs endpoint
def test_compare_programs_missing_params(client):
    response = client.get("/analysis/compare_programs")
    assert response.status_code == 400
    assert response.text == "Please input school and major"

def test_compare_programs_all_params(client):
    response = client.get("/analysis/compare_programs", query_string = {"university": "NUS", "major": "Quantitative Finance"})
    assert response.status_code == 200